# Station 2.2 - Authentication & Proxy

## Overview
Implement JWT-based authentication and create a reverse proxy to Open WebUI. Handle user registration, login, token generation, and secure request forwarding to backend services.

## Learning Objectives
- Implement JWT authentication in FastAPI
- Create secure password hashing and verification
- Build reverse proxy functionality
- Handle authentication middleware and dependencies

---

## 🎯 GENERATION PROMPT

Create authentication and proxy system for Atomic Cat AI middleware:

**File: middleware/auth.py**

Create the following components:

**1. JWT Token Management**:
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token with expiration"""
    # Use settings.JWT_SECRET and settings.JWT_ALGORITHM
    # Default expiration: settings.JWT_EXPIRATION_HOURS
    
def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    # Raise HTTPException 401 if invalid
```

**2. Authentication Dependency**:
```python
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Extract and verify user from JWT token"""
    # Extract token from credentials
    # Verify token
    # Return user data from payload
    # Raise HTTPException 401 if invalid
```

**3. Pydantic Models**:
```python
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=3, max_length=50)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class User(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime
```

**4. Authentication Endpoints** (in main.py):
```python
from fastapi import APIRouter
from redis import Redis

auth_router = APIRouter(prefix="/api/auth", tags=["authentication"])

@auth_router.post("/register", response_model=Token)
async def register(user: UserRegister, redis: Redis = Depends(get_redis)):
    """Register new user"""
    # Check if user exists in Redis (key: user:{email})
    # If exists, raise HTTPException 400 "User already exists"
    # Hash password
    # Generate unique user ID (uuid4)
    # Store in Redis: SET user:{email} JSON with {id, email, username, hashed_password, created_at}
    # Create JWT token with user data
    # Return token and user info

@auth_router.post("/login", response_model=Token)
async def login(credentials: UserLogin, redis: Redis = Depends(get_redis)):
    """Login existing user"""
    # Get user from Redis
    # If not found, raise HTTPException 401 "Invalid credentials"
    # Verify password
    # If invalid, raise HTTPException 401 "Invalid credentials"
    # Create JWT token
    # Return token and user info

@auth_router.get("/me", response_model=User)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    # Return current user data
```

**5. Open WebUI Proxy** (middleware/proxy.py):
```python
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
import httpx

proxy_router = APIRouter(prefix="/api/openwebui", tags=["proxy"])

@proxy_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_openwebui(
    request: Request,
    path: str,
    current_user: dict = Depends(get_current_user)
):
    """Proxy requests to Open WebUI with authentication"""
    # Build target URL: f"{settings.OPENWEBUI_URL}/{path}"
    # Get request body if present
    # Forward headers (except Host, Content-Length)
    # Add X-User-Id header with current_user["id"]
    
    async with httpx.AsyncClient() as client:
        # Make request to Open WebUI
        # If streaming response, use StreamingResponse
        # Otherwise return Response with same status/headers/body
        # Handle connection errors with HTTPException 503
```

**6. Redis Dependency** (add to main.py):
```python
from redis import Redis
from typing import Generator

def get_redis() -> Generator[Redis, None, None]:
    """Dependency for Redis client"""
    client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        client.close()
```

**Requirements**:
1. Use bcrypt for password hashing (strong, industry-standard)
2. JWT tokens include: user_id, email, username, exp (expiration)
3. Tokens expire after configured hours (default 24)
4. All passwords must be at least 8 characters
5. Email validation using Pydantic EmailStr
6. Store users in Redis as JSON strings
7. Proxy forwards all HTTP methods to Open WebUI
8. Proxy adds user context to forwarded requests
9. Handle streaming responses from Open WebUI (for chat)
10. Include proper error handling and logging

**Output**: Complete authentication system with JWT, user management, and Open WebUI proxy.

---

## ✅ VALIDATION PROMPT

Validate authentication and proxy implementation:

### File Structure
- [ ] `middleware/auth.py` exists
- [ ] `middleware/proxy.py` exists  
- [ ] Authentication endpoints added to `main.py`
- [ ] Redis dependency added to `main.py`

### JWT Implementation
- [ ] `hash_password()` uses bcrypt via pwd_context
- [ ] `verify_password()` checks hashed passwords correctly
- [ ] `create_access_token()`:
  - Uses settings.JWT_SECRET
  - Uses settings.JWT_ALGORITHM (HS256)
  - Sets expiration timestamp (exp claim)
  - Includes user data in payload
- [ ] `verify_token()`:
  - Verifies signature with JWT_SECRET
  - Checks expiration
  - Raises HTTPException 401 for invalid tokens
  - Returns decoded payload

### Authentication Endpoints
- [ ] **POST /api/auth/register**:
  - Validates email format and password length
  - Checks if user already exists (409 Conflict)
  - Hashes password before storing
  - Generates unique user ID (UUID)
  - Stores user in Redis with key `user:{email}`
  - Returns JWT token and user info
- [ ] **POST /api/auth/login**:
  - Retrieves user from Redis
  - Verifies password hash
  - Returns 401 for invalid credentials
  - Returns JWT token and user info
- [ ] **GET /api/auth/me**:
  - Requires authentication (Depends on get_current_user)
  - Returns current user information

### Pydantic Models
- [ ] `UserRegister` has email (EmailStr), password (min 8 chars), username
- [ ] `UserLogin` has email and password
- [ ] `Token` has access_token, token_type, user dict
- [ ] `User` has id, email, username, created_at

### Security Dependency
- [ ] `get_current_user()` dependency:
  - Uses HTTPBearer for Authorization header
  - Extracts token from "Bearer {token}"
  - Calls verify_token()
  - Returns user data
  - Raises 401 if token invalid

### Proxy Implementation
- [ ] Proxy router at `/api/openwebui`
- [ ] Handles all HTTP methods (GET, POST, PUT, DELETE, PATCH)
- [ ] Requires authentication
- [ ] Forwards requests to settings.OPENWEBUI_URL
- [ ] Preserves request:
  - Body content
  - Query parameters
  - Headers (excluding Host, Content-Length)
- [ ] Adds `X-User-Id` header with authenticated user ID
- [ ] Handles streaming responses (for chat completions)
- [ ] Returns same status code and headers as Open WebUI
- [ ] Handles connection errors gracefully (503 Service Unavailable)

### Redis Integration
- [ ] `get_redis()` dependency creates Redis client
- [ ] Uses settings.REDIS_URL
- [ ] Enables `decode_responses=True` for string handling
- [ ] Properly closes connection after use
- [ ] User data stored as JSON strings in Redis

### Commands to Run
```bash
cd middleware

# Test password hashing
python3 -c "
from auth import hash_password, verify_password
hashed = hash_password('testpass123')
print('Hash:', hashed)
print('Verify:', verify_password('testpass123', hashed))
print('Wrong:', verify_password('wrongpass', hashed))
"

# Start middleware
docker compose up -d middleware redis

# Wait for startup
sleep 5

# Test registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@atomic.cat",
    "password": "testpass123",
    "username": "testuser"
  }' | jq .

# Should return token and user info

# Extract token for next requests
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@atomic.cat",
    "password": "testpass123"
  }' | jq -r .access_token)

echo "Token: $TOKEN"

# Test /me endpoint
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# Should return user info

# Test proxy (requires Open WebUI running)
curl http://localhost:8000/api/openwebui/api/models \
  -H "Authorization: Bearer $TOKEN" | jq .

# Check Redis for user data
docker compose exec redis redis-cli GET "user:test@atomic.cat"
```

### Security Checks
- [ ] Passwords are never stored in plain text
- [ ] JWT secret is loaded from environment (not hardcoded)
- [ ] Tokens have expiration times
- [ ] Invalid tokens return 401, not 500
- [ ] Duplicate registration returns 409, not 500
- [ ] User data in Redis doesn't include password hash in responses

### Expected Results
- Users can register with email, username, password
- Registered users can login and receive JWT
- JWT is required for authenticated endpoints
- Token verification works correctly
- Expired tokens are rejected
- Proxy forwards requests to Open WebUI with user context
- Streaming responses work (important for chat)
- Redis stores user data correctly

---

## Notes
- This is a simplified auth system (production would use database + refresh tokens)
- Consider rate limiting for auth endpoints (prevent brute force)
- Open WebUI might have its own auth - this middleware adds a layer
- Next station (2.3) will use this auth for chat endpoint
- Streaming is critical for chat - test with Open WebUI chat completions
