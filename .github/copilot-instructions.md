# GitHub Copilot Instructions for Atomic Cat AI Project

## Project Context

You are assisting with **Atomic Cat AI** - a multi-user AI voice assistant with a retro 1940s atomic-era aesthetic. This is a learning project using the "Vibe Code" methodology where students use AI to generate code from detailed prompts and then validate the results.

## Tech Stack

### Backend & Infrastructure
- **Open WebUI** (port 3000) - Chat interface with model management
- **Ollama / llama.cpp** (port 11434) - Local LLM inference engine
- **FastAPI** (port 8000) - Python middleware and API gateway
- **Redis** (port 6379) - Caching and pub/sub messaging
- **Qdrant** (port 6333) - Vector database for embeddings
- **Mem0 / OpenMemory MCP** - Persistent conversation memory across sessions
- **n8n** (port 5678) - Visual workflow automation platform

### Voice & Media Processing
- **LFM2.5-Audio-1.5B** - Speech-to-Text and Text-to-Speech model
- **ComfyUI** (port 8188) - AI image generation UI with SDXL models
- **Custom Voice Server** (port 8765) - Python WebSocket server for real-time voice

### Frontend
- **SvelteKit** (port 5173) - Reactive framework with SSR support
- **Tailwind CSS** - Utility-first styling framework
- **WebSocket Client** - Real-time bidirectional communication

### Multi-Agent Orchestration
- **CrewAI** - Python framework for coordinating multiple AI agents
- **n8n workflows** - Visual automation connecting agents

### Deployment
- **Docker Compose** - Multi-container orchestration
- **NVIDIA Docker** - GPU passthrough for Ollama and ComfyUI
- Two-server deployment: Server 1 (web/API), Server 2 (GPU workloads)

## Design System - Atomic Era Theme

### Color Palette (Use Exact Hex Values)
```css
/* Primary Colors */
--atomic-teal: #40E0D0;     /* Main brand color, action buttons, links */
--atomic-coral: #FF6F61;    /* Accent color, hover states, cat's choker */
--atomic-mustard: #FFD700;  /* Highlights, warnings, cat's eyes */

/* Secondary Colors */
--atomic-mint: #98FF98;     /* Success states, positive feedback */
--atomic-cream: #FFFDD0;    /* Backgrounds, cards, panels */
--atomic-charcoal: #36454F; /* Text, borders, shadows */
```

### Typography
```css
/* Display/Headings */
font-family: 'Pacifico', cursive;
/* Import: https://fonts.googleapis.com/css2?family=Pacifico&display=swap */

/* Body Text */
font-family: 'Quicksand', sans-serif;
font-weight: 400; /* regular */
font-weight: 600; /* semi-bold for emphasis */
/* Import: https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap */
```

### Visual Elements
- **Mascot**: 1940s-style black cat silhouette with:
  - Skinny, elegant body with curved posture
  - Yellow almond-shaped eyes (#FFD700)
  - Coral choker with small gem (#FF6F61)
  - Pointed ears and long curved tail
- **Style**: Googie architecture (raygun gothic)
  - Atomic starbursts (✦ ★ ✧)
  - Boomerang shapes
  - Rounded edges on containers
  - Subtle gradients
- **Animations**: 
  - Smooth transitions (300ms ease)
  - Respectful of `prefers-reduced-motion`
  - Subtle hover effects
  - Loading states with atomic spinners

### Component Style Guidelines
```css
/* Buttons */
.btn-primary {
  background: var(--atomic-teal);
  color: var(--atomic-charcoal);
  border-radius: 24px; /* pill shape */
  padding: 12px 24px;
  font-family: 'Quicksand', sans-serif;
  font-weight: 600;
  transition: all 300ms ease;
}

.btn-primary:hover {
  background: var(--atomic-coral);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 224, 208, 0.3);
}

/* Cards */
.card {
  background: var(--atomic-cream);
  border: 2px solid var(--atomic-charcoal);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 4px 4px 0 var(--atomic-charcoal);
}

/* Inputs */
.input {
  background: white;
  border: 2px solid var(--atomic-charcoal);
  border-radius: 12px;
  padding: 12px 16px;
  font-family: 'Quicksand', sans-serif;
}

.input:focus {
  outline: none;
  border-color: var(--atomic-teal);
  box-shadow: 0 0 0 3px rgba(64, 224, 208, 0.2);
}
```

## How to Use Prompt Stations

### Station Structure
Each station file has three sections:

1. **Overview** - Brief description and learning objectives
2. **🎯 Generation Prompt** - Detailed prompt for AI to generate code
3. **✅ Validation Prompt** - Checklist to verify implementation

### When Generating Code
- Read the **entire** generation prompt first
- Generate complete, working code (no placeholders like `# TODO`)
- Include error handling and logging
- Add type hints in Python, TypeScript interfaces in frontend
- Follow existing code style in the project
- Include docstrings/comments for complex logic only
- Use environment variables for configuration

### When Validating Code
- Run through the validation checklist methodically
- Test manually where specified
- Run linters if available (`ruff`, `eslint`, etc.)
- Verify docker containers start successfully
- Check logs for errors

## Code Style Preferences

### Python (FastAPI Middleware)
```python
# Use Pydantic for data validation
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str
    conversation_id: str | None = None

# Use async/await for I/O operations
async def get_user_memory(user_id: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEM0_URL}/users/{user_id}/memories")
        return response.json()

# Use structured logging
import logging
logger = logging.getLogger(__name__)

logger.info("Processing chat request", extra={
    "user_id": user_id,
    "message_length": len(message)
})

# Use dependency injection for shared resources
from fastapi import Depends

def get_redis() -> Redis:
    return Redis.from_url(REDIS_URL)

@app.post("/api/chat")
async def chat(request: ChatRequest, redis: Redis = Depends(get_redis)):
    ...
```

### SvelteKit (Frontend)
```typescript
// Use TypeScript for type safety
interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

// Use stores for shared state
import { writable } from 'svelte/store';

export const messages = writable<Message[]>([]);
export const isConnected = writable(false);

// Use Tailwind for styling (no inline styles)
<button 
  class="btn-primary hover:scale-105 transition-transform"
  on:click={handleClick}
>
  Send Message
</button>

// Use reactive declarations
$: isValid = message.length > 0 && message.length < 1000;

// Handle cleanup
onDestroy(() => {
  websocket?.close();
});
```

### Docker Compose
```yaml
# Use environment variable substitution
environment:
  - REDIS_URL=${REDIS_URL:-redis://redis:6379}
  
# Always specify health checks
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 30s
  timeout: 5s
  retries: 3
  
# Use depends_on with conditions
depends_on:
  redis:
    condition: service_healthy
    
# Use named volumes for persistence
volumes:
  - ollama_models:/root/.ollama
  
# Use shared networks
networks:
  - atomiccat
```

## Common Patterns

### WebSocket Communication
```python
# Server-side (FastAPI)
@app.websocket("/ws/voice/{session_id}")
async def voice_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            # Process audio data
            response = await process_voice(data)
            await websocket.send_json({
                "type": "transcription",
                "text": response
            })
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
```

```typescript
// Client-side (SvelteKit)
const ws = new WebSocket(`ws://localhost:8000/ws/voice/${sessionId}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'transcription') {
    messages.update(m => [...m, { role: 'user', content: data.text }]);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
  isConnected.set(false);
};
```

### Memory Integration
```python
# Store conversation memory
async def store_memory(user_id: str, message: str, response: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{MEM0_URL}/memories", json={
            "user_id": user_id,
            "messages": [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "conversation_id": conversation_id
            }
        })

# Retrieve relevant memories
async def get_relevant_memories(user_id: str, query: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MEM0_URL}/search", json={
            "user_id": user_id,
            "query": query,
            "limit": 5
        })
        memories = response.json()
        return [m["memory"] for m in memories]
```

### n8n Workflow Triggers
```python
# Trigger n8n workflow from FastAPI
async def trigger_workflow(workflow_name: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{N8N_URL}/webhook/{workflow_name}",
            json=data,
            timeout=30.0
        )

# Example: Trigger image generation
if "create an image" in message.lower():
    await trigger_workflow("image-generation", {
        "prompt": extract_image_prompt(message),
        "user_id": user_id,
        "callback_url": f"{API_URL}/callbacks/image"
    })
```

## Error Handling Patterns

### FastAPI
```python
from fastapi import HTTPException, status

# Use HTTP exceptions
if not user_exists:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### SvelteKit
```typescript
// Use try-catch for async operations
async function sendMessage() {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    messages.update(m => [...m, data]);
  } catch (error) {
    console.error('Failed to send message:', error);
    errorMessage = 'Failed to send message. Please try again.';
  }
}
```

## Testing Guidelines

### Python Tests (pytest)
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/chat", json={
            "message": "Hello",
            "user_id": "test-user"
        })
        assert response.status_code == 200
        assert "response" in response.json()
```

### Frontend Tests (Vitest + Testing Library)
```typescript
import { render, fireEvent } from '@testing-library/svelte';
import ChatInput from './ChatInput.svelte';

test('sends message on submit', async () => {
  const { getByRole } = render(ChatInput);
  const input = getByRole('textbox');
  const button = getByRole('button', { name: /send/i });
  
  await fireEvent.input(input, { target: { value: 'Hello' } });
  await fireEvent.click(button);
  
  // Assert message was sent
});
```

## Security Considerations

1. **Never commit secrets** - Use environment variables
2. **Validate all inputs** - Use Pydantic models
3. **Sanitize user content** - Prevent XSS attacks
4. **Rate limit endpoints** - Prevent abuse
5. **Use CORS properly** - Configure allowed origins
6. **Authenticate WebSocket connections** - Verify tokens
7. **Escape SQL queries** - Use parameterized queries (if using SQL)

## Performance Optimization

1. **Use Redis caching** - Cache expensive operations
2. **Implement connection pooling** - For database connections
3. **Lazy load components** - Reduce initial bundle size
4. **Use WebSocket for real-time** - Avoid polling
5. **Optimize images** - Compress and lazy load
6. **Debounce user inputs** - Reduce API calls

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SvelteKit Docs: https://kit.svelte.dev
- Tailwind CSS: https://tailwindcss.com
- Docker Compose: https://docs.docker.com/compose/
- Mem0 Docs: https://docs.mem0.ai
- n8n Docs: https://docs.n8n.io

---

**When in doubt, prioritize:**
1. Code clarity over cleverness
2. User experience over technical perfection
3. Working features over premature optimization
4. Documentation for complex logic
