# Station 1.4 - Environment Configuration

## Overview
Create comprehensive environment configuration files with all required variables for both servers. This includes secrets, API keys, URLs, and service configuration.

## Learning Objectives
- Understand environment variable management in Docker
- Learn security best practices for secrets
- Configure service discovery and networking
- Set up development vs. production environments

---

## 🎯 GENERATION PROMPT

Create a complete `.env.example` file for Atomic Cat AI with all required environment variables, organized by service category. Include descriptive comments for each variable.

**Categories and Variables**:

**1. Security & Authentication**
```bash
# JWT secret for middleware authentication (generate with: openssl rand -hex 32)
JWT_SECRET=your-jwt-secret-here-change-this

# Open WebUI secret key (generate with: openssl rand -hex 32)
WEBUI_SECRET_KEY=your-webui-secret-change-this

# n8n encryption key (generate with: openssl rand -hex 32)
N8N_ENCRYPTION_KEY=your-n8n-encryption-key-change-this

# Redis password (generate with: openssl rand -hex 16)
REDIS_PASSWORD=your-redis-password-change-this

# Qdrant API key (generate with: openssl rand -hex 16)
QDRANT_API_KEY=your-qdrant-api-key-change-this
```

**2. Server Configuration**
```bash
# Server 1 IP (leave as localhost for single-machine setup)
SERVER1_IP=localhost

# Server 2 IP (only if using separate GPU server)
# SERVER2_IP=192.168.1.101

# Public hostname for n8n webhooks
N8N_HOST=localhost

# n8n webhook URL (use public URL in production)
N8N_WEBHOOK_URL=http://localhost:5678
```

**3. AI Model Configuration**
```bash
# Ollama model to use (e.g., llama3.2, mistral, codellama)
OLLAMA_MODEL=llama3.2

# OpenAI API key (required for Mem0 embeddings, or use local)
# If using local embeddings, set to "dummy"
OPENAI_API_KEY=dummy

# Qdrant collection name
QDRANT_COLLECTION=atomic-cat-memories
```

**4. Voice Service Configuration**
```bash
# Voice model path (LFM2.5-Audio-1.5B)
VOICE_MODEL_PATH=/models/lfm2.5-audio-1.5b

# Maximum concurrent voice sessions
MAX_VOICE_SESSIONS=4

# Enable GPU for voice processing (true/false)
VOICE_GPU_ENABLED=true

# Voice Activity Detection threshold (0.0-1.0)
VAD_THRESHOLD=0.5
```

**5. ComfyUI Configuration**
```bash
# ComfyUI URL (Server 2 or localhost if same machine)
COMFYUI_URL=http://localhost:8188

# Default image generation model
COMFYUI_MODEL=sd_xl_base_1.0.safetensors

# Image generation timeout (seconds)
IMAGE_TIMEOUT=120
```

**6. Memory Service Configuration**
```bash
# Mem0 service URL (Server 2 or localhost)
MEM0_URL=http://localhost:8080

# Memory retention days (0 = forever)
MEMORY_RETENTION_DAYS=90

# Enable automatic memory summarization
MEMORY_AUTO_SUMMARIZE=true
```

**7. Frontend Configuration**
```bash
# Public API URL for frontend
PUBLIC_API_URL=http://localhost:8000

# Public WebSocket URL for frontend
PUBLIC_WS_URL=ws://localhost:8000

# Enable debug mode in frontend
PUBLIC_DEBUG=false
```

**8. Development Options**
```bash
# Enable development mode (hot reload, verbose logging)
DEV_MODE=true

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Enable CORS for development
ENABLE_CORS=true

# Allowed CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Requirements**:
1. Every variable must have a descriptive comment
2. Include example values (but mark as "CHANGE-THIS" for secrets)
3. Group variables by service/category
4. Include commands to generate secure random values
5. Provide both single-server and dual-server examples
6. Mark optional variables with comments
7. Include sensible defaults where appropriate

**Also create**:
- `.env.development.example` - Optimized for local development with all debug flags
- `.env.production.example` - Optimized for production with security hardening

**Output**: Three complete environment configuration files with comprehensive comments.

---

## ✅ VALIDATION PROMPT

Validate environment configuration files:

### File Existence
- [ ] `.env.example` exists in project root
- [ ] `.env.development.example` exists (optional but recommended)
- [ ] `.env.production.example` exists (optional but recommended)

### Required Variables Present
Check `.env.example` includes all these variables:

**Security Variables**:
- [ ] `JWT_SECRET`
- [ ] `WEBUI_SECRET_KEY`
- [ ] `N8N_ENCRYPTION_KEY`
- [ ] `REDIS_PASSWORD`
- [ ] `QDRANT_API_KEY`

**Server Configuration**:
- [ ] `SERVER1_IP`
- [ ] `N8N_HOST`
- [ ] `N8N_WEBHOOK_URL`

**AI Models**:
- [ ] `OLLAMA_MODEL`
- [ ] `OPENAI_API_KEY` (with "dummy" option documented)
- [ ] `QDRANT_COLLECTION`

**Voice Service**:
- [ ] `VOICE_MODEL_PATH`
- [ ] `MAX_VOICE_SESSIONS`
- [ ] `VOICE_GPU_ENABLED`
- [ ] `VAD_THRESHOLD`

**ComfyUI**:
- [ ] `COMFYUI_URL`
- [ ] `COMFYUI_MODEL`
- [ ] `IMAGE_TIMEOUT`

**Memory Service**:
- [ ] `MEM0_URL`
- [ ] `MEMORY_RETENTION_DAYS`
- [ ] `MEMORY_AUTO_SUMMARIZE`

**Frontend**:
- [ ] `PUBLIC_API_URL`
- [ ] `PUBLIC_WS_URL`
- [ ] `PUBLIC_DEBUG`

**Development**:
- [ ] `DEV_MODE`
- [ ] `LOG_LEVEL`
- [ ] `ENABLE_CORS`
- [ ] `CORS_ORIGINS`

### Documentation Quality
- [ ] Each variable has a descriptive comment
- [ ] Security-sensitive variables marked "CHANGE-THIS"
- [ ] Optional variables are marked as optional
- [ ] Includes commands to generate random secrets (e.g., `openssl rand -hex 32`)
- [ ] Variables are logically grouped by service
- [ ] Single-machine and multi-machine setups are documented

### Security Best Practices
- [ ] No actual secrets or API keys in example files
- [ ] All secret variables use placeholder values
- [ ] Comments warn about changing default values
- [ ] `.env.example` is safe to commit to git
- [ ] Actual `.env` file is in `.gitignore`

### Usability Checks
- [ ] Can copy `.env.example` to `.env` and run with minimal changes
- [ ] Has sensible defaults for development
- [ ] Production configuration template is more restrictive
- [ ] Comments explain when to use which values

### Commands to Run
```bash
# Copy example to actual .env
cp .env.example .env

# Verify all variables are defined (should not show "not set")
docker compose config 2>&1 | grep "not set"

# Generate secure random values for secrets
echo "JWT_SECRET=$(openssl rand -hex 32)"
echo "WEBUI_SECRET_KEY=$(openssl rand -hex 32)"
echo "N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)"
echo "REDIS_PASSWORD=$(openssl rand -hex 16)"
echo "QDRANT_API_KEY=$(openssl rand -hex 16)"

# Check .env file is in .gitignore
grep "^\.env$" .gitignore

# Verify example files are NOT in .gitignore
! grep "\.env\.example" .gitignore
```

### Integration Test
After creating `.env`:
```bash
# Test Server 1 configuration
docker compose config | grep -v "WARNING"

# Test Server 2 configuration (if applicable)
docker compose -f docker-compose.server2.yml config | grep -v "WARNING"

# Verify no undefined variables
docker compose config 2>&1 | grep -i "variable" | grep -i "not set"
# Should return empty (no undefined variables)
```

### Expected Results
- All required environment variables are documented
- Example files are comprehensive and well-commented
- Security best practices are followed
- Easy to customize for different deployment scenarios
- Ready to start services in next module

### Next Steps
After validation, generate actual secrets:
```bash
# Create actual .env file
cp .env.example .env

# Generate and replace secrets
sed -i "s/your-jwt-secret-here-change-this/$(openssl rand -hex 32)/" .env
sed -i "s/your-webui-secret-change-this/$(openssl rand -hex 32)/" .env
sed -i "s/your-n8n-encryption-key-change-this/$(openssl rand -hex 32)/" .env
sed -i "s/your-redis-password-change-this/$(openssl rand -hex 16)/" .env
sed -i "s/your-qdrant-api-key-change-this/$(openssl rand -hex 16)/" .env

# Verify .env is excluded from git
git status | grep -v ".env"
```

---

## Notes
- Keep `.env` file secure and never commit it
- Rotate secrets regularly in production
- Use different secrets for dev/staging/prod environments
- Consider using secret management tools (Vault, AWS Secrets Manager) for production
- Some variables can be overridden at runtime with `docker compose up -e VAR=value`
- MODULE-2 will use these environment variables in the middleware
