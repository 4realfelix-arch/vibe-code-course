# Station 2.6 - WebSocket Hub for Real-Time Communication

## Overview
Implement a WebSocket hub for real-time bidirectional communication between frontend and backend. Support chat streaming, voice session management, workflow notifications, and presence tracking.

## Learning Objectives
- Build WebSocket servers with FastAPI
- Manage concurrent WebSocket connections
- Implement pub/sub patterns with Redis
- Handle connection lifecycle (connect, disconnect, reconnect)
- Broadcast messages to specific users or rooms

---

## 🎯 GENERATION PROMPT

Create a WebSocket hub for Atomic Cat AI with multiple channels:

**File: middleware/websocket_hub.py**

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Dict, Set
import json
import asyncio
import logging
from datetime import datetime
from redis import Redis
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

ws_router = APIRouter()

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        # user_id -> Set[WebSocket]
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # conversation_id -> Set[WebSocket]
        self.conversation_rooms: Dict[str, Set[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str, conversation_id: str = None):
        """Accept WebSocket connection"""
        await websocket.accept()
        
        # Add to user connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        
        # Add to conversation room if specified
        if conversation_id:
            if conversation_id not in self.conversation_rooms:
                self.conversation_rooms[conversation_id] = set()
            self.conversation_rooms[conversation_id].add(websocket)
        
        logger.info(f"WebSocket connected: user={user_id}, conversation={conversation_id}")
        
    def disconnect(self, websocket: WebSocket, user_id: str, conversation_id: str = None):
        """Remove WebSocket connection"""
        # Remove from user connections
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        # Remove from conversation room
        if conversation_id and conversation_id in self.conversation_rooms:
            self.conversation_rooms[conversation_id].discard(websocket)
            if not self.conversation_rooms[conversation_id]:
                del self.conversation_rooms[conversation_id]
        
        logger.info(f"WebSocket disconnected: user={user_id}, conversation={conversation_id}")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to all connections of a user"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected
            for conn in disconnected:
                self.active_connections[user_id].discard(conn)
    
    async def send_to_conversation(self, message: dict, conversation_id: str):
        """Send message to all participants in a conversation"""
        if conversation_id in self.conversation_rooms:
            disconnected = []
            for connection in self.conversation_rooms[conversation_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            # Clean up disconnected
            for conn in disconnected:
                self.conversation_rooms[conversation_id].discard(conn)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connections"""
        for user_connections in self.active_connections.values():
            for connection in user_connections:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

async def verify_ws_token(token: str) -> dict:
    """Verify JWT token for WebSocket connections"""
    from auth import verify_token
    try:
        payload = verify_token(token)
        return payload
    except:
        return None

@ws_router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    token: str = Query(...),
    conversation_id: str = Query(None)
):
    """
    WebSocket endpoint for chat
    
    Messages format:
    Client -> Server:
    {
        "type": "message",
        "content": "Hello!",
        "conversation_id": "uuid"
    }
    
    Server -> Client:
    {
        "type": "message|system|error",
        "content": "Response text",
        "timestamp": "ISO8601",
        "metadata": {...}
    }
    """
    # Verify token
    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    user_id = user["id"]
    await manager.connect(websocket, user_id, conversation_id)
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "system",
            "content": "Connected to Atomic Cat AI",
            "timestamp": datetime.now().isoformat(),
            "user": user
        })
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            
            message_type = data.get("type", "message")
            
            if message_type == "message":
                # Handle chat message
                content = data.get("content", "")
                conv_id = data.get("conversation_id", conversation_id)
                
                # Echo back (actual chat handled by /api/chat/message)
                await websocket.send_json({
                    "type": "received",
                    "content": content,
                    "conversation_id": conv_id,
                    "timestamp": datetime.now().isoformat()
                })
                
            elif message_type == "ping":
                # Heartbeat
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            
            elif message_type == "typing":
                # Broadcast typing indicator to conversation
                if conversation_id:
                    await manager.send_to_conversation({
                        "type": "typing",
                        "user_id": user_id,
                        "username": user.get("username", ""),
                        "timestamp": datetime.now().isoformat()
                    }, conversation_id)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id, conversation_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id, conversation_id)

@ws_router.websocket("/ws/notifications")
async def websocket_notifications(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    WebSocket endpoint for system notifications
    
    Receives:
    - Workflow completion notifications
    - Memory updates
    - System alerts
    """
    # Verify token
    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    user_id = user["id"]
    await manager.connect(websocket, user_id)
    
    try:
        # Subscribe to Redis pubsub for user notifications
        redis_client = await aioredis.from_url(settings.REDIS_URL)
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"notifications:{user_id}")
        
        # Listen for notifications from Redis
        async def redis_listener():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        await websocket.send_json(data)
                    except:
                        pass
        
        # Start listener task
        listener_task = asyncio.create_task(redis_listener())
        
        # Also listen for client messages (like heartbeat)
        while True:
            try:
                data = await websocket.receive_json()
                if data.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                break
        
        listener_task.cancel()
        await pubsub.unsubscribe(f"notifications:{user_id}")
        await redis_client.close()
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"Notification WebSocket error: {e}")
        manager.disconnect(websocket, user_id)

@ws_router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    total_connections = sum(len(conns) for conns in manager.active_connections.values())
    total_conversations = len(manager.conversation_rooms)
    
    return {
        "total_connections": total_connections,
        "active_users": len(manager.active_connections),
        "active_conversations": total_conversations,
        "timestamp": datetime.now().isoformat()
    }

# Helper function to publish notifications
async def publish_notification(user_id: str, notification: dict):
    """Publish notification to user via Redis pubsub"""
    redis_client = await aioredis.from_url(settings.REDIS_URL)
    try:
        await redis_client.publish(
            f"notifications:{user_id}",
            json.dumps(notification)
        )
    finally:
        await redis_client.close()
```

**Add to main.py**:
```python
from websocket_hub import ws_router
app.include_router(ws_router)
```

**Update requirements.txt**:
```
redis[hiredis]==5.0.1
```

**Requirements**:
1. Support multiple WebSocket endpoints (chat, notifications, voice)
2. Manage user connections and conversation rooms
3. Authenticate WebSocket connections with JWT
4. Implement pub/sub pattern with Redis for notifications
5. Handle reconnection gracefully
6. Send heartbeat/ping-pong for connection health
7. Clean up disconnected clients
8. Provide statistics endpoint
9. Support broadcasting to specific users or conversations
10. Handle errors without crashing other connections

**Output**: Complete WebSocket hub with connection management and pub/sub.

---

## ✅ VALIDATION PROMPT

Validate WebSocket hub implementation:

### File Structure
- [ ] `middleware/websocket_hub.py` exists
- [ ] WebSocket router imported and included in main.py
- [ ] Redis async client in requirements.txt

### ConnectionManager Class
- [ ] Maintains `active_connections` dict (user_id -> Set[WebSocket])
- [ ] Maintains `conversation_rooms` dict (conversation_id -> Set[WebSocket])
- [ ] `connect()` method accepts WebSocket and adds to appropriate sets
- [ ] `disconnect()` method removes WebSocket and cleans empty sets
- [ ] `send_personal_message()` sends to all user connections
- [ ] `send_to_conversation()` sends to conversation room
- [ ] `broadcast()` sends to all connections
- [ ] Handles disconnected sockets gracefully

### Authentication
- [ ] `verify_ws_token()` validates JWT tokens
- [ ] Returns user payload if valid
- [ ] Returns None if invalid
- [ ] WebSocket closes with code 1008 for invalid tokens

### WebSocket Endpoints

**/ws/chat**:
- [ ] Requires `token` query parameter
- [ ] Optional `conversation_id` query parameter
- [ ] Verifies authentication before accepting connection
- [ ] Sends welcome message on connect
- [ ] Handles message types:
  - `message` - chat messages (echoes back)
  - `ping` - heartbeat (responds with pong)
  - `typing` - typing indicators (broadcasts to conversation)
- [ ] Cleans up on disconnect
- [ ] Logs connections and disconnections

**/ws/notifications**:
- [ ] Requires `token` query parameter
- [ ] Subscribes to Redis pubsub channel `notifications:{user_id}`
- [ ] Forwards Redis messages to WebSocket
- [ ] Handles ping/pong heartbeat
- [ ] Unsubscribes and closes Redis on disconnect

### Statistics Endpoint
- [ ] **GET /ws/stats** returns:
  - Total connection count
  - Number of active users
  - Number of active conversations
  - Timestamp
- [ ] No authentication required

### Redis Integration
- [ ] Uses `redis.asyncio` for pub/sub
- [ ] Subscribes to user-specific channels
- [ ] Publishes notifications via `publish_notification()`
- [ ] Properly closes Redis connections

### Commands to Run
```bash
# Test WebSocket with websocat (install: cargo install websocat)
# Get token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@atomic.cat","password":"testpass123"}' \
  | jq -r .access_token)

echo "Token: $TOKEN"

# Test chat WebSocket
websocat "ws://localhost:8000/ws/chat?token=$TOKEN" <<EOF
{"type": "message", "content": "Hello WebSocket!"}
{"type": "ping"}
EOF

# Test with Node.js (if websocat not available)
node -e "
const WebSocket = require('ws');
const token = '$TOKEN';
const ws = new WebSocket(\`ws://localhost:8000/ws/chat?token=\${token}\`);

ws.on('open', () => {
  console.log('Connected');
  ws.send(JSON.stringify({type: 'message', content: 'Hello!'}));
});

ws.on('message', (data) => {
  console.log('Received:', data.toString());
});

ws.on('error', (error) => {
  console.error('Error:', error);
});
"

# Check WebSocket stats
curl http://localhost:8000/ws/stats | jq .

# Test notification publishing (from Python)
docker compose exec middleware python3 -c "
import asyncio
import sys
sys.path.append('/app')
from websocket_hub import publish_notification

async def test():
    await publish_notification('user-id', {
        'type': 'workflow_complete',
        'workflow_id': 'test-123',
        'message': 'Image generated!'
    })

asyncio.run(test())
"
```

### Frontend Integration Test
Create simple HTML client:
```html
<!DOCTYPE html>
<html>
<head><title>WS Test</title></head>
<body>
<div id="messages"></div>
<script>
const token = 'YOUR_TOKEN_HERE';
const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);

ws.onopen = () => {
  console.log('Connected');
  ws.send(JSON.stringify({type: 'ping'}));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  document.getElementById('messages').innerHTML += 
    `<p>${data.type}: ${JSON.stringify(data)}</p>`;
};

ws.onerror = (error) => console.error('Error:', error);
</script>
</body>
</html>
```

### Expected Results
- WebSocket connections authenticate successfully
- Chat messages are echoed back
- Ping/pong heartbeat works
- Typing indicators broadcast to conversation
- Notifications delivered via Redis pubsub
- Disconnections handled cleanly
- Stats show accurate connection counts
- Multiple connections per user work
- Connection manager prevents memory leaks

---

## Notes
- WebSocket connections bypass standard CORS
- Token must be sent as query parameter (not header for browser WebSocket)
- Redis pub/sub enables horizontal scaling (multiple middleware instances)
- Voice WebSocket (station 3.2) will be separate endpoint
- Frontend (MODULE-4) will use this hub for real-time updates
- Consider rate limiting for WebSocket messages in production
- Heartbeat prevents idle connection timeouts
