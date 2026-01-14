# Station 2.1 - FastAPI Middleware Setup

## Overview
Set up the FastAPI middleware application that acts as an API gateway between the SvelteKit frontend and backend services (Open WebUI, Mem0, n8n). This middleware handles authentication, request routing, and service orchestration.

## Learning Objectives
- Build FastAPI applications with proper project structure
- Implement CORS for frontend-backend communication
- Set up structured logging and error handling
- Configure dependency injection for shared resources
- Create health check endpoints

---

## 🎯 GENERATION PROMPT

Create a production-ready FastAPI middleware application for Atomic Cat AI with the following structure:

**File: middleware/main.py**
- FastAPI app initialization with metadata:
  - Title: "Atomic Cat AI Middleware"
  - Description: "API Gateway for multi-agent AI voice assistant"
  - Version: "1.0.0"
- CORS middleware configuration:
  - Allow origins from environment variable `CORS_ORIGINS` (comma-separated)
  - Allow credentials: true
  - Allow all methods and headers
- Include routers for (to be created in next stations):
  - `/api/auth` - Authentication
  - `/api/chat` - Chat endpoints
  - `/api/memory` - Memory operations
  - `/api/workflows` - n8n workflow triggers
  - `/ws` - WebSocket connections
- Root endpoint `/` returning JSON:
  ```json
  {
    "service": "Atomic Cat AI Middleware",
    "version": "1.0.0",
    "status": "operational"
  }
  ```
- Health check endpoint `/health` returning:
  ```json
  {
    "status": "healthy",
    "timestamp": "<ISO 8601 timestamp>",
    "services": {
      "redis": "connected|disconnected",
      "ollama": "connected|disconnected",
      "open_webui": "connected|disconnected"
    }
  }
  ```

**File: middleware/config.py**
- Use Pydantic Settings for configuration management
- Load from environment variables:
  ```python
  class Settings(BaseSettings):
      # Server
      HOST: str = "0.0.0.0"
      PORT: int = 8000
      
      # Security
      JWT_SECRET: str
      JWT_ALGORITHM: str = "HS256"
      JWT_EXPIRATION_HOURS: int = 24
      
      # Services
      REDIS_URL: str
      OPENWEBUI_URL: str
      OLLAMA_URL: str
      QDRANT_URL: str
      QDRANT_API_KEY: str
      N8N_WEBHOOK_URL: str
      MEM0_URL: str
      
      # CORS
      CORS_ORIGINS: str = "http://localhost:5173"
      
      # Logging
      LOG_LEVEL: str = "INFO"
      
      class Config:
          env_file = ".env"
          case_sensitive = True
  ```
- Global `settings` instance

**File: middleware/requirements.txt**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
httpx==0.26.0
redis==5.0.1
websockets==12.0
```

**File: middleware/Dockerfile**
- Use Python 3.11-slim as base
- Set working directory to `/app`
- Copy requirements.txt and install dependencies
- Copy application code
- Expose port 8000
- CMD: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

**File: middleware/__init__.py**
- Empty file for Python package

**Requirements**:
1. Use async/await for all I/O operations
2. Include proper error handling with HTTPException
3. Use dependency injection for shared resources (Redis, HTTP clients)
4. Structure code for testability
5. Include type hints throughout
6. Add docstrings for main functions
7. Use structured logging (JSON format)
8. Health check should actually test connections (not just return static data)

**Output**: Complete, production-ready FastAPI application with all files.

---

## ✅ VALIDATION PROMPT

Validate the FastAPI middleware setup:

### File Structure
- [ ] `middleware/main.py` exists
- [ ] `middleware/config.py` exists
- [ ] `middleware/requirements.txt` exists
- [ ] `middleware/Dockerfile` exists
- [ ] `middleware/__init__.py` exists

### main.py Validation
- [ ] FastAPI app initialized with proper metadata (title, description, version)
- [ ] CORS middleware configured:
  - Reads origins from environment
  - Allows credentials
  - Allows all methods and headers
- [ ] Root endpoint `/` returns service info
- [ ] Health check endpoint `/health` exists and returns:
  - Overall status
  - Timestamp
  - Individual service statuses (redis, ollama, open_webui)
- [ ] Router includes planned for future stations (as comments or placeholders)
- [ ] Uses async functions for endpoints

### config.py Validation
- [ ] Uses Pydantic `BaseSettings`
- [ ] All required settings defined:
  - Server configuration (HOST, PORT)
  - Security (JWT_SECRET, JWT_ALGORITHM)
  - Service URLs (REDIS_URL, OPENWEBUI_URL, etc.)
  - CORS_ORIGINS
  - LOG_LEVEL
- [ ] Has `Config` class with `env_file = ".env"`
- [ ] Settings are case-sensitive
- [ ] Provides sensible defaults where appropriate
- [ ] Global `settings` instance created

### requirements.txt Validation
- [ ] FastAPI version pinned
- [ ] Uvicorn with standard extras (for better performance)
- [ ] Pydantic and pydantic-settings for config
- [ ] python-jose for JWT handling
- [ ] passlib for password hashing
- [ ] httpx for async HTTP requests
- [ ] redis for Redis client
- [ ] websockets for WebSocket support
- [ ] All versions are compatible

### Dockerfile Validation
- [ ] Uses Python 3.11-slim (or later)
- [ ] Sets WORKDIR to `/app`
- [ ] Copies requirements.txt first (Docker layer caching)
- [ ] Installs dependencies with pip
- [ ] Copies application code
- [ ] Exposes port 8000
- [ ] CMD runs uvicorn with:
  - `--host 0.0.0.0`
  - `--port 8000`
  - `--reload` (for development)

### Code Quality
- [ ] All functions have type hints
- [ ] Async functions used for I/O operations
- [ ] Error handling with HTTPException
- [ ] No hardcoded values (uses config)
- [ ] Proper imports and no circular dependencies

### Commands to Run
```bash
cd middleware

# Check Python syntax
python3 -m py_compile main.py config.py

# Validate requirements can be installed
pip install --dry-run -r requirements.txt

# Build Docker image
docker build -t atomic-cat-middleware:test .

# Should complete without errors

# Test running the container (requires .env)
docker run --env-file ../.env -p 8000:8000 atomic-cat-middleware:test

# In another terminal, test endpoints:
curl http://localhost:8000/
# Should return service info

curl http://localhost:8000/health
# Should return health status
```

### Integration Test
```bash
# Start middleware with docker compose
docker compose up -d middleware

# Wait for startup
sleep 5

# Test root endpoint
curl http://localhost:8000/ | jq .
# Should see: {"service": "Atomic Cat AI Middleware", ...}

# Test health endpoint
curl http://localhost:8000/health | jq .
# Should see: {"status": "healthy", "services": {...}}

# Check logs
docker compose logs middleware
# Should show startup messages, no errors

# Stop service
docker compose down middleware
```

### Expected Results
- FastAPI application starts without errors
- All endpoints respond correctly
- Health check actually tests service connections
- Docker image builds successfully
- Configuration loads from environment
- CORS is properly configured
- Ready for authentication implementation in Station 2.2

---

## Notes
- The `--reload` flag in Dockerfile is for development only (remove in production)
- Health check should timeout quickly if services are unavailable
- Consider adding request logging middleware for debugging
- Next station will add JWT authentication
- Use `httpx.AsyncClient` for making requests to other services
