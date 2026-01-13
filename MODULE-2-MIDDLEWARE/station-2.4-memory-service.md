# Station 2.4 - Memory Service Integration

## Overview
Create dedicated endpoints for memory management - search, add, delete, and list user memories. Provide direct access to Mem0 functionality through the middleware API.

## Learning Objectives
- Build CRUD operations for memory management
- Implement memory search with embeddings
- Handle user-specific data isolation
- Create admin endpoints for memory management

---

## 🎯 GENERATION PROMPT

Create comprehensive memory service endpoints for Atomic Cat AI:

**File: middleware/memory_client.py**

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import httpx
import logging

memory_router = APIRouter(prefix="/api/memory", tags=["memory"])
logger = logging.getLogger(__name__)

# Pydantic Models
class MemoryCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    metadata: Optional[dict] = None

class MemorySearch(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)

class Memory(BaseModel):
    id: str
    content: str
    user_id: str
    created_at: datetime
    metadata: Optional[dict] = None

class MemoryList(BaseModel):
    memories: List[Memory]
    total: int

@memory_router.post("/add", response_model=Memory)
async def add_memory(
    memory: MemoryCreate,
    current_user: dict = Depends(get_current_user)
):
    """Add a new memory for the current user"""
    user_id = current_user["id"]
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{settings.MEM0_URL}/memories",
                json={
                    "user_id": user_id,
                    "messages": [
                        {"role": "user", "content": memory.content}
                    ],
                    "metadata": memory.metadata or {}
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return Memory(
                id=data.get("id", ""),
                content=memory.content,
                user_id=user_id,
                created_at=datetime.now(),
                metadata=memory.metadata
            )
    except httpx.HTTPError as e:
        logger.error(f"Failed to add memory: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")

@memory_router.post("/search", response_model=MemoryList)
async def search_memories(
    search: MemorySearch,
    current_user: dict = Depends(get_current_user)
):
    """Search user's memories using semantic search"""
    user_id = current_user["id"]
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{settings.MEM0_URL}/search",
                json={
                    "user_id": user_id,
                    "query": search.query,
                    "limit": search.limit
                }
            )
            response.raise_for_status()
            data = response.json()
            
            memories = [
                Memory(
                    id=mem.get("id", ""),
                    content=mem.get("memory", mem.get("content", "")),
                    user_id=user_id,
                    created_at=datetime.fromisoformat(mem.get("created_at", datetime.now().isoformat())),
                    metadata=mem.get("metadata")
                )
                for mem in data.get("memories", [])
            ]
            
            return MemoryList(memories=memories, total=len(memories))
    except httpx.HTTPError as e:
        logger.error(f"Failed to search memories: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")

@memory_router.get("/list", response_model=MemoryList)
async def list_memories(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: dict = Depends(get_current_user)
):
    """List all memories for the current user with pagination"""
    user_id = current_user["id"]
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{settings.MEM0_URL}/memories",
                params={
                    "user_id": user_id,
                    "limit": limit,
                    "offset": offset
                }
            )
            response.raise_for_status()
            data = response.json()
            
            memories = [
                Memory(
                    id=mem.get("id", ""),
                    content=mem.get("memory", mem.get("content", "")),
                    user_id=user_id,
                    created_at=datetime.fromisoformat(mem.get("created_at", datetime.now().isoformat())),
                    metadata=mem.get("metadata")
                )
                for mem in data.get("memories", [])
            ]
            
            return MemoryList(
                memories=memories,
                total=data.get("total", len(memories))
            )
    except httpx.HTTPError as e:
        logger.error(f"Failed to list memories: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")

@memory_router.delete("/{memory_id}")
async def delete_memory(
    memory_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a specific memory"""
    user_id = current_user["id"]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(
                f"{settings.MEM0_URL}/memories/{memory_id}",
                params={"user_id": user_id}
            )
            response.raise_for_status()
            
            return {"message": "Memory deleted successfully", "id": memory_id}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Memory not found")
        logger.error(f"Failed to delete memory: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")
    except httpx.HTTPError as e:
        logger.error(f"Failed to delete memory: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")

@memory_router.delete("/clear")
async def clear_all_memories(
    current_user: dict = Depends(get_current_user)
):
    """Clear all memories for the current user"""
    user_id = current_user["id"]
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(
                f"{settings.MEM0_URL}/memories",
                params={"user_id": user_id}
            )
            response.raise_for_status()
            
            return {"message": "All memories cleared successfully"}
    except httpx.HTTPError as e:
        logger.error(f"Failed to clear memories: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")

@memory_router.get("/stats")
async def get_memory_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get memory statistics for the current user"""
    user_id = current_user["id"]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get total count
            response = await client.get(
                f"{settings.MEM0_URL}/memories",
                params={"user_id": user_id, "limit": 1}
            )
            response.raise_for_status()
            data = response.json()
            
            total_memories = data.get("total", 0)
            
            return {
                "user_id": user_id,
                "total_memories": total_memories,
                "username": current_user.get("username", "")
            }
    except httpx.HTTPError as e:
        logger.error(f"Failed to get memory stats: {e}")
        raise HTTPException(status_code=503, detail="Memory service unavailable")
```

**Add to main.py**:
```python
from memory_client import memory_router
app.include_router(memory_router)
```

**Requirements**:
1. All endpoints require authentication
2. Users can only access their own memories
3. Search uses semantic search (embeddings)
4. Pagination support for list endpoint
5. Proper error handling and logging
6. Return 503 if Mem0 unavailable
7. Return 404 if specific memory not found
8. Include statistics endpoint
9. Support metadata on memories

**Output**: Complete memory service integration with CRUD operations.

---

## ✅ VALIDATION PROMPT

Validate memory service implementation:

### File Structure
- [ ] `middleware/memory_client.py` exists
- [ ] Memory router imported and included in main.py

### Pydantic Models
- [ ] `MemoryCreate` has content (1-2000 chars) and optional metadata
- [ ] `MemorySearch` has query and limit (1-50, default 10)
- [ ] `Memory` has id, content, user_id, created_at, metadata
- [ ] `MemoryList` has memories array and total count

### Endpoints

**POST /api/memory/add**:
- [ ] Requires authentication
- [ ] Creates memory in Mem0 with user_id
- [ ] Returns Memory object
- [ ] Returns 503 if Mem0 unavailable

**POST /api/memory/search**:
- [ ] Requires authentication
- [ ] Searches user's memories only
- [ ] Uses semantic search (embeddings)
- [ ] Returns MemoryList with results
- [ ] Limits results to requested amount
- [ ] Returns 503 if Mem0 unavailable

**GET /api/memory/list**:
- [ ] Requires authentication
- [ ] Lists user's memories with pagination
- [ ] Supports limit (1-200, default 50) and offset parameters
- [ ] Returns MemoryList with total count
- [ ] Returns 503 if Mem0 unavailable

**DELETE /api/memory/{memory_id}**:
- [ ] Requires authentication
- [ ] Deletes specific memory
- [ ] Verifies user_id matches
- [ ] Returns 404 if memory not found
- [ ] Returns 503 if Mem0 unavailable

**DELETE /api/memory/clear**:
- [ ] Requires authentication
- [ ] Clears all user memories
- [ ] Uses longer timeout (30s)
- [ ] Returns success message
- [ ] Returns 503 if Mem0 unavailable

**GET /api/memory/stats**:
- [ ] Requires authentication
- [ ] Returns total memory count for user
- [ ] Includes user_id and username
- [ ] Returns 503 if Mem0 unavailable

### Security
- [ ] All endpoints use `get_current_user` dependency
- [ ] Users cannot access other users' memories
- [ ] All requests include user_id in Mem0 calls
- [ ] No memory IDs exposed without ownership verification

### Commands to Run
```bash
# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@atomic.cat","password":"testpass123"}' \
  | jq -r .access_token)

# Add a memory
curl -X POST http://localhost:8000/api/memory/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "I love retro 1940s atomic design",
    "metadata": {"category": "preferences"}
  }' | jq .

# Add more memories
curl -X POST http://localhost:8000/api/memory/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "My favorite color is teal"}' | jq .

# Search memories
curl -X POST http://localhost:8000/api/memory/search \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are my design preferences?",
    "limit": 5
  }' | jq .

# List all memories
curl -X GET "http://localhost:8000/api/memory/list?limit=10&offset=0" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Get memory stats
curl -X GET http://localhost:8000/api/memory/stats \
  -H "Authorization: Bearer $TOKEN" | jq .

# Delete a specific memory (use ID from list response)
MEMORY_ID="some-memory-id"
curl -X DELETE "http://localhost:8000/api/memory/$MEMORY_ID" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Clear all memories (be careful!)
# curl -X DELETE http://localhost:8000/api/memory/clear \
#   -H "Authorization: Bearer $TOKEN" | jq .
```

### Expected Results
- Memories are created and stored per user
- Search returns semantically relevant memories
- List endpoint supports pagination
- Delete removes specific memories
- Stats show accurate count
- All operations are user-isolated
- 503 errors when Mem0 is unavailable

---

## Notes
- Mem0 uses embeddings for semantic search (not keyword matching)
- Memories persist across sessions
- Clear endpoint is destructive - consider confirmation in frontend
- Next station (2.5) will add workflow service endpoints
- Consider rate limiting for add/delete operations in production
