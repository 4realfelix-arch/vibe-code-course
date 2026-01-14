# Station 1.2 - Docker Compose Core Services (Server 1)

## Overview
Configure Docker Compose for Server 1 with all core services: Open WebUI, Ollama, Redis, Qdrant, n8n, and the middleware/frontend containers. This creates the foundation for the AI assistant's backend infrastructure.

## Learning Objectives
- Understand Docker Compose service definitions and networking
- Configure GPU passthrough for AI model inference
- Set up service dependencies and health checks
- Manage environment variables and secrets

---

## 🎯 GENERATION PROMPT

Create a production-ready `docker-compose.yml` for Server 1 of Atomic Cat AI with the following services:

**Service: open-webui**
- Image: `ghcr.io/open-webui/open-webui:main`
- Port: `3000:8080` (internal port 8080 mapped to external 3000)
- Environment variables:
  - `OLLAMA_BASE_URL=http://ollama:11434`
  - `ENABLE_RAG_WEB_SEARCH=true`
  - `ENABLE_IMAGE_GENERATION=true`
  - `WEBUI_AUTH=true`
  - `WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}`
- Volumes:
  - `open-webui-data:/app/backend/data`
- Depends on: `ollama`, `redis`
- Restart: `unless-stopped`

**Service: ollama**
- Image: `ollama/ollama:latest`
- Port: `11434:11434`
- Environment: `OLLAMA_HOST=0.0.0.0`
- Volumes:
  - `ollama_models:/root/.ollama`
- Deploy resources (GPU):
  ```yaml
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
  ```
- Restart: `unless-stopped`
- Healthcheck:
  - Command: `curl -f http://localhost:11434/api/tags || exit 1`
  - Interval: 30s
  - Timeout: 10s
  - Retries: 3

**Service: redis**
- Image: `redis:7-alpine`
- Port: `6379:6379` (for development, remove in production)
- Command: `redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}`
- Volumes:
  - `redis_data:/data`
- Restart: `unless-stopped`
- Healthcheck:
  - Command: `redis-cli --no-auth-warning -a ${REDIS_PASSWORD} ping | grep PONG`
  - Interval: 30s
  - Timeout: 5s
  - Retries: 3

**Service: qdrant**
- Image: `qdrant/qdrant:latest`
- Port: `6333:6333`
- Volumes:
  - `qdrant_storage:/qdrant/storage`
- Environment:
  - `QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}`
- Restart: `unless-stopped`

**Service: n8n**
- Image: `n8nio/n8n:latest`
- Port: `5678:5678`
- Environment:
  - `N8N_HOST=${N8N_HOST:-localhost}`
  - `N8N_PORT=5678`
  - `N8N_PROTOCOL=http`
  - `WEBHOOK_URL=${N8N_WEBHOOK_URL:-http://localhost:5678}`
  - `N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}`
  - `DB_TYPE=sqlite`
- Volumes:
  - `n8n_data:/home/node/.n8n`
  - `./workflows:/workflows:ro`
- Restart: `unless-stopped`

**Service: middleware**
- Build:
  - Context: `./middleware`
  - Dockerfile: `Dockerfile`
- Port: `8000:8000`
- Environment:
  - `REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379`
  - `OPENWEBUI_URL=http://open-webui:8080`
  - `OLLAMA_URL=http://ollama:11434`
  - `QDRANT_URL=http://qdrant:6333`
  - `QDRANT_API_KEY=${QDRANT_API_KEY}`
  - `N8N_WEBHOOK_URL=http://n8n:5678`
  - `MEM0_URL=${MEM0_URL:-http://host.docker.internal:8765}`
  - `JWT_SECRET=${JWT_SECRET}`
- Depends on:
  - `redis` (condition: service_healthy)
  - `ollama` (condition: service_healthy)
  - `open-webui`
- Restart: `unless-stopped`
- Volumes:
  - `./middleware:/app` (for development hot reload)

**Service: frontend**
- Build:
  - Context: `./frontend`
  - Dockerfile: `Dockerfile`
- Port: `5173:5173`
- Environment:
  - `PUBLIC_API_URL=http://localhost:8000`
  - `PUBLIC_WS_URL=ws://localhost:8000`
- Volumes:
  - `./frontend:/app` (for development)
  - `/app/node_modules` (anonymous volume to prevent overwrite)
- Command: `npm run dev -- --host`
- Depends on: `middleware`
- Restart: `unless-stopped`

**Network Configuration**:
- Create a custom bridge network named `atomiccat`
- All services should be on this network

**Volume Definitions**:
```yaml
volumes:
  open-webui-data:
  ollama_models:
  redis_data:
  qdrant_storage:
  n8n_data:
```

**Requirements**:
1. Use `${VAR}` syntax for all environment variables
2. Include `version: "3.8"` at the top
3. Add comments explaining each service
4. Use depends_on with service_healthy conditions where health checks exist
5. Configure proper restart policies
6. Use named volumes for persistence
7. Include the shared `atomiccat` network

**Output**: Complete `docker-compose.yml` file with proper YAML formatting and comments.

---

## ✅ VALIDATION PROMPT

Validate the Docker Compose configuration meets all requirements:

### YAML Syntax Validation
```bash
# Validate YAML syntax
docker compose -f docker-compose.yml config

# Should output the parsed configuration without errors
```

### Service Configuration Checks
- [ ] **open-webui**:
  - Port mapping is `3000:8080`
  - Has `OLLAMA_BASE_URL=http://ollama:11434`
  - Depends on `ollama` and `redis`
  - Uses persistent volume `open-webui-data`
  - Has `WEBUI_SECRET_KEY` from environment

- [ ] **ollama**:
  - Has GPU reservation with `nvidia` driver
  - Uses persistent volume for models
  - Has health check with curl command
  - Port `11434` exposed

- [ ] **redis**:
  - Uses `redis:7-alpine` image
  - Has password protection via `--requirepass ${REDIS_PASSWORD}`
  - Enables append-only file (AOF) persistence
  - Has health check that verifies authentication works
  - Uses persistent volume `redis_data`

- [ ] **qdrant**:
  - Port `6333` exposed
  - Has API key protection
  - Uses persistent volume for storage

- [ ] **n8n**:
  - Port `5678` exposed
  - Has `N8N_ENCRYPTION_KEY` set
  - Mounts `./workflows` directory as read-only
  - Uses persistent volume for data

- [ ] **middleware**:
  - Builds from `./middleware` directory
  - Port `8000` exposed
  - Has all required environment variables:
    - `REDIS_URL` (with password)
    - `OPENWEBUI_URL`
    - `OLLAMA_URL`
    - `QDRANT_URL` and `QDRANT_API_KEY`
    - `N8N_WEBHOOK_URL`
    - `MEM0_URL`
    - `JWT_SECRET`
  - Depends on `redis` with `service_healthy` condition
  - Has volume mount for development

- [ ] **frontend**:
  - Builds from `./frontend` directory
  - Port `5173` exposed
  - Has `PUBLIC_API_URL` and `PUBLIC_WS_URL`
  - Has anonymous volume for `node_modules`
  - Runs dev server with `--host` flag
  - Depends on `middleware`

### Network Configuration
- [ ] Custom network `atomiccat` is defined under `networks:`
- [ ] All services use the `atomiccat` network
- [ ] Network allows inter-service communication

### Volume Configuration
- [ ] All volumes are defined in top-level `volumes:` section
- [ ] Named volumes are used (not bind mounts for data)
- [ ] Volumes include:
  - `open-webui-data`
  - `ollama_models`
  - `redis_data`
  - `qdrant_storage`
  - `n8n_data`

### Environment Variables
- [ ] All sensitive values use `${VAR}` syntax
- [ ] No hardcoded passwords or secrets
- [ ] Has sensible defaults with `${VAR:-default}` where appropriate

### Health Checks
- [ ] Ollama has curl-based health check
- [ ] Redis has authentication-aware health check
- [ ] Both have appropriate intervals and timeouts

### Best Practices
- [ ] Uses `unless-stopped` restart policy
- [ ] Includes comments for each service
- [ ] Uses official images from trusted sources
- [ ] Service names are lowercase with hyphens
- [ ] Proper indentation (2 spaces)

### Commands to Run
```bash
# Validate configuration
docker compose config

# Check for undefined environment variables
docker compose config 2>&1 | grep -i "variable.*not set"

# Verify GPU configuration (if NVIDIA GPU available)
docker compose config | grep -A 5 "devices:"

# Test service dependencies
docker compose config | grep -A 3 "depends_on:"

# Verify network configuration
docker compose config | grep -A 5 "networks:"
```

### Expected Results
- YAML is valid and parseable
- All services are properly configured
- Network configuration allows service communication
- GPU passthrough configured correctly for Ollama
- Health checks are functional
- Environment variables are properly templated
- Ready to create `.env.example` in Station 1.4

---

## Notes
- Don't start services yet (wait for Station 1.4 to create `.env`)
- If you don't have an NVIDIA GPU, the compose file will still work but ollama will use CPU
- Development mode uses volume mounts for hot reloading
- Production deployment would remove development mounts (covered in MODULE-6)
