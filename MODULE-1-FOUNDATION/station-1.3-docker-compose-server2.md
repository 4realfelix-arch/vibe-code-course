# Station 1.3 - Docker Compose Server 2 (GPU Workloads)

## Overview
Configure Docker Compose for Server 2 with GPU-intensive services: ComfyUI for image generation, voice server for STT/TTS, and Mem0 for memory management. This optional second server handles compute-heavy AI tasks.

## Learning Objectives
- Configure multiple Docker Compose files for distributed deployment
- Set up ComfyUI with SDXL models
- Deploy voice processing services
- Integrate Mem0 memory service

---

## 🎯 GENERATION PROMPT

Create `docker-compose.server2.yml` for GPU-intensive services of Atomic Cat AI:

**Service: comfyui**
- Image: `ghcr.io/ai-dock/comfyui:latest-cuda`
- Ports:
  - `8188:8188` (ComfyUI web interface)
  - `8118:8118` (Comfy-Manager)
- Environment:
  - `GPU=all`
  - `COMFYUI_PORT_HOST=8188`
- Volumes:
  - `comfyui_data:/data`
  - `comfyui_output:/output`
- Deploy resources:
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

**Service: voice-server**
- Build:
  - Context: `./voice-server`
  - Dockerfile: `Dockerfile`
- Port: `8765:8765`
- Environment:
  - `MODEL_PATH=/models/lfm2.5-audio-1.5b`
  - `GPU_ENABLED=true`
  - `REDIS_URL=redis://:${REDIS_PASSWORD}@${SERVER1_IP:-host.docker.internal}:6379`
  - `MAX_CONCURRENT_SESSIONS=4`
- Volumes:
  - `voice_models:/models`
  - `./voice-server:/app` (for development)
- Deploy resources:
  ```yaml
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
  ```
- Restart: `unless-stopped`

**Service: mem0**
- Image: `mem0ai/mem0:latest`
- Port: `8080:8080`
- Environment:
  - `MEM0_HOST=0.0.0.0`
  - `MEM0_PORT=8080`
  - `OPENAI_API_KEY=${OPENAI_API_KEY:-dummy}`
  - `QDRANT_URL=http://${SERVER1_IP:-host.docker.internal}:6333`
  - `QDRANT_API_KEY=${QDRANT_API_KEY}`
- Volumes:
  - `mem0_data:/data`
- Restart: `unless-stopped`
- Healthcheck:
  - Command: `curl -f http://localhost:8080/health || exit 1`
  - Interval: 30s
  - Timeout: 10s
  - Retries: 3

**Network Configuration**:
- Use external network `atomiccat` (created in docker-compose.yml)
- Set `external: true` in network definition

**Volume Definitions**:
```yaml
volumes:
  comfyui_data:
  comfyui_output:
  voice_models:
  mem0_data:
```

**Requirements**:
1. Use `version: "3.8"`
2. Include comments for each service
3. Use `${VAR}` syntax for environment variables
4. Support connection to Server 1 via `SERVER1_IP` environment variable
5. Each GPU service should have explicit GPU reservations
6. Use named volumes for model storage and data persistence
7. Reference the external `atomiccat` network

**Output**: Complete `docker-compose.server2.yml` file.

---

## ✅ VALIDATION PROMPT

Validate Server 2 Docker Compose configuration:

### YAML Syntax Validation
```bash
# Validate YAML syntax
docker compose -f docker-compose.server2.yml config

# Should parse without errors
```

### Service Configuration Checks
- [ ] **comfyui**:
  - Uses CUDA-enabled image
  - Port `8188` mapped for web interface
  - Has GPU reservation with nvidia driver
  - Uses persistent volumes for data and output
  - Port `8118` exposed for Comfy-Manager

- [ ] **voice-server**:
  - Builds from `./voice-server` directory
  - Port `8765` exposed
  - Has environment variables:
    - `MODEL_PATH` pointing to voice model location
    - `GPU_ENABLED=true`
    - `REDIS_URL` with Server 1 IP (or host.docker.internal for same machine)
    - `MAX_CONCURRENT_SESSIONS=4`
  - Has GPU reservation (count: 1 for voice server)
  - Uses persistent volume for models
  - Has development volume mount

- [ ] **mem0**:
  - Port `8080` exposed
  - Has environment variables:
    - `MEM0_HOST=0.0.0.0`
    - `QDRANT_URL` pointing to Server 1
    - `QDRANT_API_KEY`
  - Uses persistent volume `mem0_data`
  - Has health check
  - Has `OPENAI_API_KEY` with dummy default

### Network Configuration
- [ ] References external network `atomiccat`
- [ ] Network is marked as `external: true`
- [ ] All services are on the `atomiccat` network

### Volume Configuration
- [ ] All volumes defined in top-level `volumes:` section
- [ ] Named volumes for:
  - `comfyui_data` (ComfyUI workflows and settings)
  - `comfyui_output` (generated images)
  - `voice_models` (LFM2.5 Audio model)
  - `mem0_data` (memory database)

### GPU Configuration
- [ ] ComfyUI requests all available GPUs
- [ ] Voice server requests 1 GPU
- [ ] Both use `nvidia` driver
- [ ] Capabilities include `[gpu]`

### Inter-Server Communication
- [ ] Services can connect to Server 1 via `SERVER1_IP` variable
- [ ] Fallback to `host.docker.internal` for single-machine setup
- [ ] Redis URL includes Server 1 IP
- [ ] Qdrant URL includes Server 1 IP

### Commands to Run
```bash
# Validate configuration
docker compose -f docker-compose.server2.yml config

# Check GPU configuration
docker compose -f docker-compose.server2.yml config | grep -A 5 "devices:"

# Verify external network reference
docker compose -f docker-compose.server2.yml config | grep -A 3 "external:"

# Check volume definitions
docker compose -f docker-compose.server2.yml config | grep -A 20 "^volumes:"
```

### Integration Validation
If both Server 1 and Server 2 are on same machine:
```bash
# Create network first (from Server 1)
docker network create atomiccat

# Start Server 2 services
docker compose -f docker-compose.server2.yml up -d

# Verify they can reach Server 1
docker compose -f docker-compose.server2.yml exec mem0 curl -f http://host.docker.internal:6333
```

If on separate machines:
```bash
# Server 2 needs to connect to Server 1 IP
export SERVER1_IP=192.168.1.100  # Replace with actual IP

# Services should use this IP to connect
docker compose -f docker-compose.server2.yml config | grep SERVER1_IP
```

### Expected Results
- YAML is valid and parseable
- All GPU services have proper GPU reservations
- Services can communicate with Server 1
- External network is properly referenced
- Volume mounts are correctly configured
- Ready for environment configuration in Station 1.4

---

## Notes
- Server 2 is optional - you can run everything on Server 1 (CPU mode)
- For single-machine setup, use `host.docker.internal` to access Server 1
- For multi-machine setup, set `SERVER1_IP` environment variable
- ComfyUI models (SDXL) will be downloaded on first run (~6GB)
- Voice model (LFM2.5) needs to be downloaded separately (covered in MODULE-3)
- This server requires more GPU VRAM (12GB+ recommended)
