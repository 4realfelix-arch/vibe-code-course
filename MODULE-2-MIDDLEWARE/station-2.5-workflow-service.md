# Station 2.5 - Workflow Service Integration

## Overview
Create endpoints to trigger and monitor n8n workflows for image generation, multi-agent tasks, and custom automations. Enable the middleware to orchestrate complex AI workflows.

## Learning Objectives
- Integrate with n8n workflow automation
- Implement webhook-based workflow triggering
- Handle async workflow execution
- Monitor workflow status and results

---

## 🎯 GENERATION PROMPT

Create workflow service integration for Atomic Cat AI with n8n:

**File: middleware/workflow_service.py**

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import uuid4
import httpx
import logging
import json

workflow_router = APIRouter(prefix="/api/workflows", tags=["workflows"])
logger = logging.getLogger(__name__)

# Pydantic Models
class WorkflowTrigger(BaseModel):
    workflow_name: str = Field(..., pattern="^[a-z0-9-]+$")
    payload: Dict[str, Any] = Field(default_factory=dict)
    callback_url: Optional[str] = None

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    negative_prompt: Optional[str] = None
    width: int = Field(default=1024, ge=512, le=2048)
    height: int = Field(default=1024, ge=512, le=2048)
    steps: int = Field(default=30, ge=10, le=100)

class MultiAgentTask(BaseModel):
    task_description: str = Field(..., min_length=1, max_length=2000)
    agents: List[str] = Field(default=["researcher", "writer"])
    max_iterations: int = Field(default=5, ge=1, le=20)

class WorkflowResponse(BaseModel):
    workflow_id: str
    workflow_name: str
    status: str
    triggered_at: datetime
    message: str

@workflow_router.post("/trigger", response_model=WorkflowResponse)
async def trigger_workflow(
    trigger: WorkflowTrigger,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Trigger a custom n8n workflow"""
    workflow_id = str(uuid4())
    user_id = current_user["id"]
    
    # Build payload with user context
    full_payload = {
        "workflow_id": workflow_id,
        "user_id": user_id,
        "username": current_user.get("username", ""),
        "timestamp": datetime.now().isoformat(),
        **trigger.payload
    }
    
    # Add callback URL if provided
    if trigger.callback_url:
        full_payload["callback_url"] = trigger.callback_url
    
    # Trigger workflow in background
    background_tasks.add_task(
        execute_workflow,
        trigger.workflow_name,
        full_payload
    )
    
    logger.info(f"Triggered workflow {trigger.workflow_name} for user {user_id}")
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        workflow_name=trigger.workflow_name,
        status="triggered",
        triggered_at=datetime.now(),
        message=f"Workflow {trigger.workflow_name} has been triggered"
    )

@workflow_router.post("/image-generation", response_model=WorkflowResponse)
async def trigger_image_generation(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Trigger ComfyUI image generation workflow"""
    workflow_id = str(uuid4())
    user_id = current_user["id"]
    
    payload = {
        "workflow_id": workflow_id,
        "user_id": user_id,
        "prompt": request.prompt,
        "negative_prompt": request.negative_prompt or "blurry, low quality, distorted",
        "width": request.width,
        "height": request.height,
        "steps": request.steps,
        "model": settings.COMFYUI_MODEL,
        "callback_url": f"{settings.PUBLIC_API_URL}/api/workflows/callback/{workflow_id}"
    }
    
    background_tasks.add_task(
        execute_workflow,
        "image-generation",
        payload
    )
    
    logger.info(f"Triggered image generation for user {user_id}")
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        workflow_name="image-generation",
        status="triggered",
        triggered_at=datetime.now(),
        message="Image generation started. You will be notified when complete."
    )

@workflow_router.post("/multi-agent-task", response_model=WorkflowResponse)
async def trigger_multi_agent_task(
    task: MultiAgentTask,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Trigger multi-agent CrewAI workflow"""
    workflow_id = str(uuid4())
    user_id = current_user["id"]
    
    payload = {
        "workflow_id": workflow_id,
        "user_id": user_id,
        "task": task.task_description,
        "agents": task.agents,
        "max_iterations": task.max_iterations,
        "callback_url": f"{settings.PUBLIC_API_URL}/api/workflows/callback/{workflow_id}"
    }
    
    background_tasks.add_task(
        execute_workflow,
        "multi-agent-crew",
        payload
    )
    
    logger.info(f"Triggered multi-agent task for user {user_id}")
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        workflow_name="multi-agent-crew",
        status="triggered",
        triggered_at=datetime.now(),
        message=f"Multi-agent task started with {len(task.agents)} agents"
    )

@workflow_router.post("/callback/{workflow_id}")
async def workflow_callback(
    workflow_id: str,
    payload: Dict[str, Any]
):
    """Receive callbacks from n8n workflows"""
    logger.info(f"Received callback for workflow {workflow_id}")
    
    # Store result in Redis for frontend retrieval
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        redis_client.setex(
            f"workflow:{workflow_id}",
            3600,  # 1 hour TTL
            json.dumps(payload)
        )
        logger.info(f"Stored workflow result for {workflow_id}")
    finally:
        redis_client.close()
    
    # TODO: Optionally notify user via WebSocket
    
    return {"status": "received", "workflow_id": workflow_id}

@workflow_router.get("/status/{workflow_id}")
async def get_workflow_status(
    workflow_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get status and result of a workflow"""
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        result = redis_client.get(f"workflow:{workflow_id}")
        
        if result:
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "result": json.loads(result)
            }
        else:
            return {
                "workflow_id": workflow_id,
                "status": "pending",
                "message": "Workflow is still running or has expired"
            }
    finally:
        redis_client.close()

@workflow_router.get("/list")
async def list_available_workflows():
    """List all available n8n workflows"""
    workflows = [
        {
            "name": "image-generation",
            "description": "Generate images using ComfyUI and SDXL",
            "parameters": ["prompt", "negative_prompt", "width", "height", "steps"]
        },
        {
            "name": "multi-agent-crew",
            "description": "Execute multi-agent tasks with CrewAI",
            "parameters": ["task", "agents", "max_iterations"]
        },
        {
            "name": "memory-search",
            "description": "Advanced memory search with context",
            "parameters": ["query", "context"]
        }
    ]
    
    return {"workflows": workflows, "total": len(workflows)}

async def execute_workflow(workflow_name: str, payload: Dict[str, Any]):
    """Execute n8n workflow via webhook"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.N8N_WEBHOOK_URL}/webhook/{workflow_name}",
                json=payload
            )
            response.raise_for_status()
            logger.info(f"Successfully executed workflow {workflow_name}")
    except httpx.HTTPError as e:
        logger.error(f"Failed to execute workflow {workflow_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error executing workflow {workflow_name}: {e}")
```

**Add to main.py**:
```python
from workflow_service import workflow_router
from redis import Redis

app.include_router(workflow_router)
```

**Add to config.py**:
```python
COMFYUI_MODEL: str = "sd_xl_base_1.0.safetensors"
PUBLIC_API_URL: str = "http://localhost:8000"
```

**Requirements**:
1. Execute workflows asynchronously using BackgroundTasks
2. Store workflow results in Redis with TTL
3. Support callback mechanism for workflow completion
4. Provide status endpoint to check workflow progress
5. Include user context in all workflow payloads
6. Handle workflow execution errors gracefully
7. Log all workflow triggers and completions
8. Generate unique workflow IDs

**Output**: Complete workflow service integration with n8n.

---

## ✅ VALIDATION PROMPT

Validate workflow service implementation:

### File Structure
- [ ] `middleware/workflow_service.py` exists
- [ ] Workflow router imported and included in main.py
- [ ] Config variables added (COMFYUI_MODEL, PUBLIC_API_URL)

### Pydantic Models
- [ ] `WorkflowTrigger` has workflow_name and payload
- [ ] `ImageGenerationRequest` has prompt, dimensions, steps
- [ ] `MultiAgentTask` has task_description and agents list
- [ ] `WorkflowResponse` has workflow_id, status, timestamp

### Endpoints

**POST /api/workflows/trigger**:
- [ ] Requires authentication
- [ ] Generates unique workflow_id
- [ ] Adds user context to payload
- [ ] Executes workflow in background
- [ ] Returns immediately with workflow_id
- [ ] Logs trigger event

**POST /api/workflows/image-generation**:
- [ ] Requires authentication
- [ ] Validates image parameters (dimensions, steps)
- [ ] Creates payload with ComfyUI parameters
- [ ] Includes callback URL
- [ ] Triggers "image-generation" workflow
- [ ] Returns workflow_id

**POST /api/workflows/multi-agent-task**:
- [ ] Requires authentication
- [ ] Validates task description and agents
- [ ] Creates payload with CrewAI parameters
- [ ] Triggers "multi-agent-crew" workflow
- [ ] Returns workflow_id

**POST /api/workflows/callback/{workflow_id}**:
- [ ] No authentication required (called by n8n)
- [ ] Stores result in Redis with workflow_id key
- [ ] Sets 1-hour TTL on result
- [ ] Logs callback reception
- [ ] Returns success status

**GET /api/workflows/status/{workflow_id}**:
- [ ] Requires authentication
- [ ] Retrieves result from Redis
- [ ] Returns "completed" if result exists
- [ ] Returns "pending" if no result
- [ ] Includes result data when available

**GET /api/workflows/list**:
- [ ] No authentication required
- [ ] Lists all available workflows
- [ ] Includes workflow descriptions
- [ ] Shows required parameters

### Background Execution
- [ ] Uses FastAPI BackgroundTasks
- [ ] Doesn't block HTTP response
- [ ] Handles execution errors without crashing
- [ ] Logs all execution attempts

### Helper Functions

**execute_workflow()**:
- [ ] Makes POST to n8n webhook URL
- [ ] Sends payload as JSON
- [ ] Has 60s timeout
- [ ] Handles HTTP errors gracefully
- [ ] Logs success and failures

### Commands to Run
```bash
# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@atomic.cat","password":"testpass123"}' \
  | jq -r .access_token)

# List available workflows
curl http://localhost:8000/api/workflows/list | jq .

# Trigger image generation
curl -X POST http://localhost:8000/api/workflows/image-generation \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "1940s retro atomic cat with yellow eyes",
    "width": 1024,
    "height": 1024,
    "steps": 30
  }' | jq .

# Save workflow_id from response
WORKFLOW_ID="..."

# Check workflow status
curl http://localhost:8000/api/workflows/status/$WORKFLOW_ID \
  -H "Authorization: Bearer $TOKEN" | jq .

# Trigger multi-agent task
curl -X POST http://localhost:8000/api/workflows/multi-agent-task \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Research the history of atomic age design",
    "agents": ["researcher", "writer", "critic"],
    "max_iterations": 5
  }' | jq .

# Trigger custom workflow
curl -X POST http://localhost:8000/api/workflows/trigger \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_name": "memory-search",
    "payload": {
      "query": "atomic design preferences",
      "context": "ui themes"
    }
  }' | jq .

# Check middleware logs for workflow triggers
docker compose logs middleware | grep "Triggered workflow"
```

### Expected Results
- Workflows trigger without blocking response
- Workflow IDs are unique and trackable
- Status endpoint shows pending until callback received
- Callbacks store results in Redis
- All workflows include user context
- Errors are logged but don't crash service

---

## Notes
- n8n workflows must be created separately (MODULE-5)
- Workflow results expire after 1 hour in Redis
- Consider WebSocket notifications for workflow completion (MODULE-2.6)
- Image generation can take 30-120 seconds depending on GPU
- Multi-agent tasks can take several minutes
- Next station (2.6) will add WebSocket hub for real-time updates
