# Station 2.3 - Chat Endpoint with Memory

## Overview
Create the core chat endpoint that integrates memory retrieval, LLM interaction, and workflow triggering. This endpoint searches user memories, builds context-enhanced prompts, forwards to Open WebUI, stores conversations in Mem0, and triggers relevant workflows.

## Learning Objectives
- Integrate multiple AI services in a single endpoint
- Implement context-aware conversation with memory
- Handle streaming responses from LLMs
- Trigger automated workflows based on conversation content
- Implement graceful degradation when services are unavailable

---

## 🎯 GENERATION PROMPT

Create the chat endpoint for Atomic Cat AI with full memory integration and workflow triggering:

**File: middleware/chat.py**

**Pydantic Models**:
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None
    stream: bool = True

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    memories_used: int
    workflow_triggered: Optional[str] = None
```

**Main Chat Endpoint**:
```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import json
import logging
from uuid import uuid4

chat_router = APIRouter(prefix="/api/chat", tags=["chat"])

logger = logging.getLogger(__name__)

@chat_router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Main chat endpoint with memory integration.
    
    Flow:
    1. Extract user ID from authentication
    2. Search Mem0 for relevant memories
    3. Build enhanced prompt with memory context
    4. Forward to Open WebUI /api/chat/completions
    5. Check response for workflow triggers
    6. Store conversation in Mem0
    7. Return response
    """
    
    user_id = current_user["id"]
    conversation_id = request.conversation_id or str(uuid4())
    
    # Step 1: Retrieve relevant memories
    memories = []
    try:
        memories = await search_memories(user_id, request.message)
        logger.info(f"Retrieved {len(memories)} memories for user {user_id}")
    except Exception as e:
        logger.warning(f"Memory retrieval failed: {e}. Continuing without memory.")
    
    # Step 2: Build enhanced prompt with memory context
    enhanced_prompt = build_prompt_with_memory(request.message, memories)
    
    # Step 3: Forward to Open WebUI
    try:
        if request.stream:
            # Return streaming response
            return StreamingResponse(
                stream_chat_response(
                    enhanced_prompt, 
                    user_id, 
                    conversation_id,
                    request.message,
                    memories
                ),
                media_type="text/event-stream"
            )
        else:
            # Return complete response
            response_text = await get_chat_completion(enhanced_prompt)
            
            # Check for workflow triggers
            workflow = check_workflow_triggers(request.message, response_text)
            if workflow:
                await trigger_workflow(workflow, {
                    "user_id": user_id,
                    "message": request.message,
                    "response": response_text
                })
            
            # Store conversation
            await store_conversation(user_id, conversation_id, request.message, response_text)
            
            return ChatResponse(
                response=response_text,
                conversation_id=conversation_id,
                memories_used=len(memories),
                workflow_triggered=workflow
            )
    except Exception as e:
        logger.error(f"Chat completion failed: {e}")
        raise HTTPException(status_code=503, detail="AI service unavailable")

async def search_memories(user_id: str, query: str, limit: int = 5) -> List[dict]:
    """Search Mem0 for relevant memories"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{settings.MEM0_URL}/search",
            json={
                "user_id": user_id,
                "query": query,
                "limit": limit
            }
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("memories", [])
        else:
            raise Exception(f"Mem0 returned {response.status_code}")

def build_prompt_with_memory(message: str, memories: List[dict]) -> str:
    """Build enhanced prompt with memory context"""
    if not memories:
        return message
    
    # Sanitize memory content to prevent prompt injection
    def sanitize_memory(mem_text: str) -> str:
        """Remove potential prompt injection patterns"""
        # Remove system-level instructions and prompt markers
        dangerous_patterns = [
            "Ignore previous instructions",
            "System:",
            "Assistant:",
            "###",
            "---",
        ]
        sanitized = mem_text
        for pattern in dangerous_patterns:
            sanitized = sanitized.replace(pattern, "")
        # Limit length per memory
        return sanitized[:200]
    
    memory_context = "\n".join([
        f"- {sanitize_memory(mem.get('memory', mem.get('content', '')))}"
        for mem in memories
    ])
    
    enhanced = f"""You are Atomic Cat AI, a helpful assistant with memory of past conversations.

**What you remember about this user:**
{memory_context}

**Current message:**
{message}

**Instructions:**
- Use the memories naturally in your response when relevant
- Don't explicitly mention "I remember" unless it adds value
- Be conversational and helpful
- If memories aren't relevant, ignore them

**Response:**"""
    
    return enhanced

async def get_chat_completion(prompt: str) -> str:
    """Get completion from Open WebUI"""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.OPENWEBUI_URL}/api/chat/completions",
            json={
                "model": settings.OLLAMA_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

async def stream_chat_response(
    prompt: str,
    user_id: str,
    conversation_id: str,
    original_message: str,
    memories: List[dict]
):
    """Stream chat response and handle side effects"""
    full_response = ""
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{settings.OPENWEBUI_URL}/api/chat/completions",
            json={
                "model": settings.OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    chunk = line[6:]  # Remove "data: " prefix
                    if chunk == "[DONE]":
                        break
                    try:
                        data = json.loads(chunk)
                        content = data["choices"][0]["delta"].get("content", "")
                        if content:
                            full_response += content
                            yield f"data: {json.dumps({'content': content})}\n\n"
                    except json.JSONDecodeError:
                        continue
    
    # After streaming completes, handle side effects
    workflow = check_workflow_triggers(original_message, full_response)
    if workflow:
        await trigger_workflow(workflow, {
            "user_id": user_id,
            "message": original_message,
            "response": full_response
        })
    
    await store_conversation(user_id, conversation_id, original_message, full_response)
    
    # Send completion event
    yield f"data: {json.dumps({'done': True, 'memories_used': len(memories), 'workflow': workflow})}\n\n"

def check_workflow_triggers(message: str, response: str) -> Optional[str]:
    """Check if conversation should trigger a workflow"""
    message_lower = message.lower()
    
    # Image generation trigger
    if any(keyword in message_lower for keyword in ["create image", "generate image", "draw", "make a picture"]):
        return "image-generation"
    
    # Multi-agent task trigger
    if any(keyword in message_lower for keyword in ["research", "analyze deeply", "detailed analysis"]):
        return "multi-agent-crew"
    
    return None

async def trigger_workflow(workflow_name: str, data: dict):
    """Trigger n8n workflow"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.post(
                f"{settings.N8N_WEBHOOK_URL}/webhook/{workflow_name}",
                json=data
            )
        logger.info(f"Triggered workflow: {workflow_name}")
    except Exception as e:
        logger.error(f"Failed to trigger workflow {workflow_name}: {e}")

async def store_conversation(user_id: str, conversation_id: str, message: str, response: str):
    """Store conversation in Mem0"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                f"{settings.MEM0_URL}/memories",
                json={
                    "user_id": user_id,
                    "messages": [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": response}
                    ],
                    "metadata": {
                        "conversation_id": conversation_id,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        logger.info(f"Stored conversation for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to store conversation: {e}")
```

**Add to main.py**:
```python
from chat import chat_router
app.include_router(chat_router)
```

**Add to config.py**:
```python
OLLAMA_MODEL: str = "llama3.2"
```

**Requirements**:
1. Handle streaming and non-streaming responses
2. Gracefully degrade if Mem0 is unavailable (continue without memory)
3. Build memory context that's clear for LLM to understand
4. Check for workflow triggers based on keywords
5. Store conversations asynchronously (don't block response)
6. Use appropriate timeouts (10s for memory, 120s for chat)
7. Include comprehensive error handling
8. Log all important events
9. Support conversation continuation with conversation_id

**Output**: Complete chat endpoint with memory integration, streaming support, and workflow triggering.

---

## ✅ VALIDATION PROMPT

Validate the chat endpoint implementation:

### File Structure
- [ ] `middleware/chat.py` exists
- [ ] Chat router imported and included in `main.py`
- [ ] `OLLAMA_MODEL` added to config.py

### Request/Response Models
- [ ] `ChatRequest` has:
  - `message` (required, 1-5000 chars)
  - `conversation_id` (optional)
  - `stream` (bool, default true)
- [ ] `ChatResponse` has:
  - `response` (string)
  - `conversation_id` (string)
  - `memories_used` (int)
  - `workflow_triggered` (optional string)

### Main Endpoint Flow
Trace through the complete flow for **POST /api/chat/message**:

**Step 1: Memory Retrieval**
- [ ] Calls `search_memories()` with user_id and message
- [ ] Catches exceptions and continues if Mem0 unavailable
- [ ] Logs number of memories retrieved
- [ ] Uses timeout of 10 seconds

**Step 2: Prompt Enhancement**
- [ ] Calls `build_prompt_with_memory()`
- [ ] If memories exist, formats them clearly
- [ ] Creates prompt that includes:
  - System context (Atomic Cat AI)
  - Memory context (formatted as list)
  - Current message
  - Instructions to use memories naturally
- [ ] If no memories, returns original message

**Step 3: LLM Interaction**
- [ ] For streaming (`request.stream=True`):
  - Returns `StreamingResponse` with media_type "text/event-stream"
  - Calls `stream_chat_response()`
- [ ] For non-streaming:
  - Calls `get_chat_completion()`
  - Returns complete response

**Step 4: Workflow Triggering**
- [ ] `check_workflow_triggers()` examines message content
- [ ] Triggers "image-generation" for image-related keywords
- [ ] Triggers "multi-agent-crew" for research keywords
- [ ] Returns None if no triggers match
- [ ] Calls `trigger_workflow()` if match found

**Step 5: Conversation Storage**
- [ ] Calls `store_conversation()` with user_id, conversation_id, message, response
- [ ] Stores in Mem0 with metadata (conversation_id, timestamp)
- [ ] Handles errors gracefully (logs but doesn't fail)

### Function Implementations

**search_memories()**:
- [ ] Makes POST request to `{MEM0_URL}/search`
- [ ] Sends user_id, query, limit
- [ ] Returns list of memory dicts
- [ ] Raises exception on non-200 status
- [ ] Has 10s timeout

**build_prompt_with_memory()**:
- [ ] Returns enhanced prompt with memory context
- [ ] Formats memories as clear list
- [ ] Includes instructions for LLM
- [ ] Returns original message if no memories

**get_chat_completion()**:
- [ ] Makes POST to `{OPENWEBUI_URL}/api/chat/completions`
- [ ] Sends model, messages, stream=False
- [ ] Extracts content from response
- [ ] Has 120s timeout
- [ ] Raises on HTTP errors

**stream_chat_response()**:
- [ ] Streams response using `httpx.stream()`
- [ ] Parses SSE format ("data: " prefix)
- [ ] Accumulates full_response
- [ ] Yields chunks as JSON
- [ ] After completion:
  - Checks workflow triggers
  - Stores conversation
  - Sends done event with metadata

**check_workflow_triggers()**:
- [ ] Checks message for image keywords
- [ ] Checks message for research keywords
- [ ] Returns workflow name or None
- [ ] Case-insensitive matching

**trigger_workflow()**:
- [ ] Makes POST to `{N8N_WEBHOOK_URL}/webhook/{workflow_name}`
- [ ] Sends user_id, message, response
- [ ] Has 30s timeout
- [ ] Logs success/failure
- [ ] Doesn't raise exceptions (handles internally)

**store_conversation()**:
- [ ] Makes POST to `{MEM0_URL}/memories`
- [ ] Sends user_id, messages array, metadata
- [ ] Has 10s timeout
- [ ] Logs success/failure
- [ ] Doesn't raise exceptions

### Error Handling
- [ ] Memory retrieval failure → logs warning, continues without memory
- [ ] Chat completion failure → raises HTTPException 503
- [ ] Workflow trigger failure → logs error, doesn't fail request
- [ ] Conversation storage failure → logs error, doesn't fail request
- [ ] All failures are logged with appropriate level

### Commands to Run
```bash
# Start all required services
docker compose up -d middleware redis open-webui ollama

# Wait for services
sleep 10

# Get auth token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@atomic.cat","password":"testpass123"}' \
  | jq -r .access_token)

# Test non-streaming chat (without Mem0)
curl -X POST http://localhost:8000/api/chat/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! My name is Alice and I love cats.",
    "stream": false
  }' | jq .

# Should return response with conversation_id

# Test streaming chat
curl -X POST http://localhost:8000/api/chat/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me a short story about a cat.",
    "stream": true
  }'

# Should stream response in SSE format

# Test workflow trigger (image generation)
curl -X POST http://localhost:8000/api/chat/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create an image of a retro atomic cat",
    "stream": false
  }' | jq .

# Should have workflow_triggered: "image-generation"

# Check logs for workflow trigger
docker compose logs middleware | grep "Triggered workflow"
```

### Expected Results
- Chat endpoint responds to messages
- Streaming and non-streaming both work
- Memory retrieval is attempted (graceful failure if Mem0 not running)
- Prompt enhancement includes memory context when available
- Workflow triggers detected correctly
- Conversations stored (if Mem0 available)
- All errors handled gracefully without crashing
- Logs show complete flow

---

## Notes
- This is the core of the AI assistant - most complex endpoint
- Memory integration is optional (graceful degradation)
- Streaming is crucial for good UX with LLMs
- Workflow triggering enables advanced features
- Next station (2.4) will implement dedicated memory service endpoints
- In production, consider caching frequently accessed memories
- Monitor timeout values and adjust based on model performance
