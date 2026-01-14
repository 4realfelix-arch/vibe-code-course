# 🔧 Troubleshooting Guide

Common issues and solutions for Atomic Cat AI development.

---

## 🐳 Docker Issues

### Services Won't Start

**Problem**: `docker compose up` fails  
**Solutions**:
```bash
# Check if .env file exists
ls -la .env

# Validate docker-compose syntax
docker compose config

# Check for port conflicts
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :5173

# View logs for specific service
docker compose logs middleware
docker compose logs -f open-webui  # follow logs

# Restart specific service
docker compose restart middleware
```

### GPU Not Detected

**Problem**: Ollama or voice-server can't access GPU  
**Solutions**:
```bash
# Verify NVIDIA driver
nvidia-smi

# Check Docker has NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Install NVIDIA Docker if missing
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Set GPU_ENABLED=false in .env if no GPU available
```

### Out of Memory

**Problem**: Container crashes with OOM  
**Solutions**:
```bash
# Check Docker memory limit
docker stats

# Increase Docker Desktop memory (Mac/Windows)
# Docker Desktop → Settings → Resources → Memory → 8GB+

# For Linux, edit /etc/docker/daemon.json:
{
  "default-ulimits": {
    "memlock": {"soft": -1, "hard": -1}
  }
}

# Use smaller models
OLLAMA_MODEL=llama3.2:1b  # Instead of larger models

# Limit concurrent sessions
MAX_VOICE_SESSIONS=2  # Instead of 4
```

### Volumes Permission Issues

**Problem**: Permission denied errors in containers  
**Solutions**:
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./middleware ./frontend ./voice-server

# Or run with correct user in docker-compose.yml:
user: "${UID}:${GID}"

# Get your UID/GID
id -u  # UID
id -g  # GID
```

---

## 🔐 Authentication Issues

### JWT Token Invalid

**Problem**: 401 Unauthorized errors  
**Solutions**:
```bash
# Verify JWT_SECRET is set
echo $JWT_SECRET

# Generate new secret
openssl rand -hex 32

# Check token expiration
# Tokens expire after JWT_EXPIRATION_HOURS (default 24)

# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"testpass"}'

# Verify token
TOKEN="your-token-here"
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### CORS Errors in Browser

**Problem**: "Access-Control-Allow-Origin" errors  
**Solutions**:
```bash
# Check CORS_ORIGINS includes frontend URL
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Restart middleware after changing .env
docker compose restart middleware

# Verify CORS headers in response
curl -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  http://localhost:8000/api/chat/message -v
```

---

## 🤖 AI Model Issues

### Model Not Found

**Problem**: Ollama says model not found  
**Solutions**:
```bash
# Pull model into Ollama
docker compose exec ollama ollama pull llama3.2

# List available models
docker compose exec ollama ollama list

# Update OLLAMA_MODEL in .env
OLLAMA_MODEL=llama3.2

# Check model is downloaded
docker compose exec ollama ls -lh /root/.ollama/models
```

### Slow Inference

**Problem**: LLM responses take too long  
**Solutions**:
```bash
# Use smaller/faster model
OLLAMA_MODEL=llama3.2:1b  # Faster than 8b

# Enable GPU acceleration (verify with nvidia-smi)
docker compose exec ollama nvidia-smi

# Increase Ollama threads (if CPU only)
docker compose exec ollama ollama run llama3.2 --num-thread 8

# Use quantized models (Q4, Q5)
docker compose exec ollama ollama pull llama3.2:q4_K_M
```

### Memory Service Fails

**Problem**: Mem0 unavailable or errors  
**Solutions**:
```bash
# Check Mem0 is running (Server 2)
curl http://localhost:8080/health

# Verify connection from middleware
docker compose exec middleware curl http://host.docker.internal:8080/health

# Check Qdrant is accessible
curl http://localhost:6333

# Set OPENAI_API_KEY or use dummy
OPENAI_API_KEY=dummy  # For local embeddings

# Fallback: Middleware works without Mem0 (graceful degradation)
```

---

## 🎤 Voice Issues

### No Audio Input/Output

**Problem**: Voice features don't work  
**Solutions**:
```bash
# Check voice server is running
curl http://localhost:8765/health

# Verify WebSocket connection
# In browser console:
const ws = new WebSocket('ws://localhost:8765/ws/voice/test?user_id=test');
ws.onopen = () => console.log('Connected');
ws.onerror = (e) => console.error('Error:', e);

# Check browser has microphone permissions
# Browser → Settings → Site Settings → Microphone

# Test audio format (should be 16kHz PCM)
# Use browser AudioContext:
const ctx = new AudioContext({sampleRate: 16000});
```

### VAD Too Sensitive/Not Sensitive

**Problem**: Voice detection triggers incorrectly  
**Solutions**:
```bash
# Adjust VAD threshold in .env
VAD_THRESHOLD=0.02  # Default
VAD_THRESHOLD=0.05  # Less sensitive (good for noisy environments)
VAD_THRESHOLD=0.01  # More sensitive (good for quiet environments)

# Adjust silence duration
# In voice_websocket.py:
max_silence_duration = 2.0  # Wait longer before ending speech
min_speech_duration = 0.5   # Require longer speech to register

# Test noise gate
NOISE_GATE_THRESHOLD=-40  # dB
```

### Barge-In Not Working

**Problem**: Can't interrupt AI speech  
**Solutions**:
```bash
# Verify TTS task is cancellable
# Check voice_websocket.py:
- Task must be stored in session.tts_task
- Must call session.cancel_tts() on speech detection
- Must handle asyncio.CancelledError

# Check logs for "Barge-in detected"
docker compose -f docker-compose.server2.yml logs voice-server | grep "Barge-in"

# Verify VAD runs during SPEAKING state
# In handle_audio_chunk():
if session.state == SessionState.SPEAKING:
    vad_result = session.vad.detect(audio_array)
```

---

## 🌐 Frontend Issues

### Blank Page

**Problem**: Frontend shows blank page  
**Solutions**:
```bash
# Check frontend is running
curl http://localhost:5173

# Check browser console for errors (F12)

# Verify API URL is correct
PUBLIC_API_URL=http://localhost:8000

# Check middleware is accessible from browser
curl http://localhost:8000/

# Rebuild frontend
cd frontend
npm run build
npm run dev
```

### WebSocket Connection Fails

**Problem**: "WebSocket connection failed" in console  
**Solutions**:
```bash
# Check WebSocket URL
PUBLIC_WS_URL=ws://localhost:8000  # Not http://

# Verify middleware WebSocket endpoint
curl http://localhost:8000/ws/stats

# Check browser WebSocket support
# In console:
'WebSocket' in window  # Should be true

# Test connection manually:
const ws = new WebSocket('ws://localhost:8000/ws/chat?token=YOUR_TOKEN');
ws.onopen = () => console.log('Connected!');
```

### Tailwind Styles Not Applying

**Problem**: Components have no styling  
**Solutions**:
```bash
# Verify Tailwind is installed
cd frontend
npm list tailwindcss

# Check tailwind.config.js exists and has content paths
cat tailwind.config.js

# Verify app.css is imported in +layout.svelte
grep "app.css" src/routes/+layout.svelte

# Rebuild CSS
npm run dev  # Restart dev server

# Check generated CSS
ls -lh .svelte-kit/build
```

---

## 🔄 Workflow Issues

### n8n Webhooks Not Triggering

**Problem**: Workflows don't execute  
**Solutions**:
```bash
# Verify n8n is running
curl http://localhost:5678

# Check webhook URL is accessible
curl -X POST http://localhost:5678/webhook/test-workflow \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Verify workflow is active in n8n UI
# n8n → Workflows → Check "Active" toggle

# Check n8n logs
docker compose logs n8n | grep webhook

# Verify N8N_WEBHOOK_URL in .env
N8N_WEBHOOK_URL=http://n8n:5678  # From middleware
N8N_WEBHOOK_URL=http://localhost:5678  # From browser
```

### ComfyUI Image Generation Fails

**Problem**: Images don't generate  
**Solutions**:
```bash
# Check ComfyUI is running
curl http://localhost:8188

# Verify GPU is available
docker compose -f docker-compose.server2.yml exec comfyui nvidia-smi

# Check models are downloaded
docker compose -f docker-compose.server2.yml exec comfyui \
  ls -lh /data/models/checkpoints/

# Download SDXL model (if missing)
# ComfyUI Manager → Install Models → SDXL Base 1.0

# Check workflow JSON is valid
# Import to ComfyUI UI and test manually
```

---

## 📊 Database Issues

### Redis Connection Refused

**Problem**: "Connection refused" to Redis  
**Solutions**:
```bash
# Check Redis is running
docker compose ps redis

# Test connection
docker compose exec redis redis-cli ping
# Should return PONG

# Test with password
docker compose exec redis redis-cli -a $REDIS_PASSWORD ping

# Verify REDIS_URL format
REDIS_URL=redis://:password@redis:6379  # From containers
REDIS_URL=redis://:password@localhost:6379  # From host
```

### Qdrant Vector Store Issues

**Problem**: Vector search not working  
**Solutions**:
```bash
# Check Qdrant is running
curl http://localhost:6333

# Verify collection exists
curl http://localhost:6333/collections

# Create collection if missing
curl -X PUT http://localhost:6333/collections/atomic-cat-memories \
  -H "Content-Type: application/json" \
  -H "api-key: $QDRANT_API_KEY" \
  -d '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    }
  }'

# Check Qdrant logs
docker compose logs qdrant
```

---

## 🚀 Performance Issues

### High CPU Usage

**Solutions**:
```bash
# Monitor CPU per container
docker stats

# Limit CPU for containers (in docker-compose.yml):
deploy:
  resources:
    limits:
      cpus: '2.0'

# Use smaller models
OLLAMA_MODEL=llama3.2:1b

# Reduce concurrent sessions
MAX_VOICE_SESSIONS=2
```

### High Memory Usage

**Solutions**:
```bash
# Monitor memory per container
docker stats

# Limit memory (in docker-compose.yml):
deploy:
  resources:
    limits:
      memory: 4G

# Clear old Docker data
docker system prune -a --volumes

# Use quantized models
ollama pull llama3.2:q4_K_M
```

---

## 🆘 Emergency Commands

### Reset Everything
```bash
# Stop all services
docker compose down
docker compose -f docker-compose.server2.yml down

# Remove all volumes (WARNING: deletes data!)
docker compose down -v

# Remove all images
docker rmi $(docker images -q atomic-cat-*)

# Rebuild from scratch
docker compose build --no-cache
docker compose up -d
```

### Check All Service Health
```bash
# One-liner health check
for service in open-webui ollama redis qdrant n8n middleware frontend; do
  echo -n "$service: "
  docker compose ps $service | grep -q "Up" && echo "✓" || echo "✗"
done
```

### View All Logs
```bash
# Follow all logs
docker compose logs -f

# Last 100 lines from all services
docker compose logs --tail=100

# Specific service with timestamps
docker compose logs -ft middleware
```

---

## 📞 Getting More Help

1. **Check logs first**: `docker compose logs [service]`
2. **Search issues**: GitHub issues in the repo
3. **Ask in discussions**: Provide error messages and logs
4. **Review station validation**: Each station has troubleshooting tips
5. **Check environment**: `docker compose config` shows final configuration

**Remember**: Most issues are environment/configuration related, not code bugs!
