# 🚀 Prompt Station Quick Reference

Quick overview of all 33 stations in the Atomic Cat AI curriculum.

## 📖 How to Use This Guide

Each station has:
- 🎯 **Generation Prompt** - Give to AI to create code
- ✅ **Validation Prompt** - Verify implementation works
- ⏱️ **Time Estimate** - Approximate completion time

---

## MODULE-1: FOUNDATION (4 hours)

### 1.1 - Project Structure (1 hour)
**Purpose**: Create complete directory structure and .gitignore  
**Key Output**: Monorepo with middleware/, frontend/, voice-server/, workflows/, scripts/, tests/, docs/  
**Validation**: tree command shows correct structure, README has quick start

### 1.2 - Docker Compose Core (1.5 hours)
**Purpose**: Configure Server 1 services  
**Key Services**: Open WebUI, Ollama (GPU), Redis, Qdrant, n8n, middleware, frontend  
**Validation**: `docker compose config` validates, all services defined with health checks

### 1.3 - Docker Compose Server 2 (1 hour)
**Purpose**: Configure GPU-intensive services  
**Key Services**: ComfyUI, voice-server, Mem0  
**Validation**: External network reference works, GPU reservations configured

### 1.4 - Environment Config (0.5 hours)
**Purpose**: Create comprehensive .env.example  
**Key Variables**: JWT_SECRET, REDIS_PASSWORD, OLLAMA_MODEL, all service URLs  
**Validation**: All 40+ variables documented with generation commands

---

## MODULE-2: MIDDLEWARE (8 hours)

### 2.1 - FastAPI Setup (1.5 hours)
**Purpose**: Initialize FastAPI app with config  
**Key Files**: main.py, config.py, requirements.txt, Dockerfile  
**Validation**: Health check endpoint works, CORS configured

### 2.2 - Auth & Proxy (2 hours)
**Purpose**: JWT authentication and Open WebUI proxy  
**Key Features**: User registration/login, password hashing, token generation, reverse proxy  
**Validation**: Register user, login, access /me endpoint, proxy to Open WebUI

### 2.3 - Chat Endpoint (2 hours)
**Purpose**: Core chat with memory integration  
**Key Features**: Memory search, prompt enhancement, streaming, workflow triggers  
**Validation**: Chat works with/without memory, streaming functions, workflows trigger

### 2.4 - Memory Service (1.5 hours)
**Purpose**: CRUD operations for Mem0  
**Key Endpoints**: add, search, list, delete, clear, stats  
**Validation**: Add memories, search semantically, list with pagination

### 2.5 - Workflow Service (1.5 hours)
**Purpose**: n8n workflow triggering  
**Key Endpoints**: trigger, image-generation, multi-agent-task, callback, status  
**Validation**: Trigger workflows, receive callbacks, check status

### 2.6 - WebSocket Hub (1.5 hours)
**Purpose**: Real-time communication  
**Key Features**: Connection management, pub/sub, chat/notifications channels  
**Validation**: Connect WebSocket, send/receive messages, heartbeat works

---

## MODULE-3: VOICE (4 hours)

### 3.1 - Voice Server (1.5 hours)
**Purpose**: PyTorch voice processing server  
**Key Features**: Model loading, transcribe, synthesize, audio format conversion  
**Validation**: Server starts, health check works, placeholder inference runs

### 3.2 - Voice WebSocket with Barge-In (2 hours)
**Purpose**: Real-time voice with interruption support  
**Key Classes**: VoiceSession, VoiceSessionManager, SimpleVAD  
**Key Feature**: Barge-in detection cancels TTS immediately  
**Validation**: User can interrupt AI mid-speech, VAD detects speech start/end

### 3.3 - Voice Pipeline (0.5 hours)
**Purpose**: End-to-end voice conversation  
**Key Features**: LLMClient, VoiceConversationManager, audio utilities  
**Validation**: Voice → transcription → LLM → TTS → voice works

---

## MODULE-4: FRONTEND (10 hours)

### 4.1 - SvelteKit Setup (2 hours)
**Purpose**: Initialize SvelteKit with atomic theme  
**Key Features**: Tailwind config, atomic colors, custom fonts, component styles  
**Validation**: Dev server runs, tailwind classes work, atomic theme applies

### 4.2 - API Stores (1 hour)
**Purpose**: Svelte stores for state management  
**Key Stores**: auth, chat, websocket, voice  
**Validation**: Stores persist, reactive updates work

### 4.3 - WebSocket Client (1.5 hours)
**Purpose**: Frontend WebSocket integration  
**Key Features**: Connection management, reconnection, event handling  
**Validation**: Connects, sends/receives, handles disconnection

### 4.4 - Main Layout (1.5 hours)
**Purpose**: Root layout with navigation  
**Key Features**: Header with cat avatar, navigation, responsive  
**Validation**: Layout renders, navigation works, responsive on mobile

### 4.5 - Chat Components (2 hours)
**Purpose**: Message list and input  
**Key Components**: ChatMessages.svelte, ChatInput.svelte  
**Validation**: Messages display, input works, markdown renders

### 4.6 - Cat Avatar (1.5 hours)
**Purpose**: Animated mascot  
**Key Features**: 6 animation states, SVG cat, smooth transitions  
**Validation**: All states animate correctly, respects prefers-reduced-motion

### 4.7 - Sidebar (1 hour)
**Purpose**: Conversation history  
**Key Features**: List conversations, select, delete, timestamps  
**Validation**: Shows conversations, selection works, updates reactively

### 4.8 - Details Panel (0.5 hours)
**Purpose**: User info and settings  
**Key Features**: Profile, memory stats, settings  
**Validation**: Displays user data, settings persist

---

## MODULE-5: INTEGRATION (8 hours)

### 5.1 - Main Page (2 hours)
**Purpose**: Chat interface assembly  
**Integration**: Layout + Chat + Avatar + Sidebar + Details  
**Validation**: Full chat experience works

### 5.2 - Login Page (1.5 hours)
**Purpose**: Authentication UI  
**Key Features**: Login/register forms, validation, routing  
**Validation**: Login works, redirects to chat, errors display

### 5.3 - n8n Workflows (2 hours)
**Purpose**: Create workflow JSON files  
**Key Workflows**: image-generation, multi-agent-crew, memory-search  
**Validation**: Import to n8n, test webhooks

### 5.4 - Docker Builds (1.5 hours)
**Purpose**: Build and test all containers  
**Key Tasks**: Build middleware, frontend, voice-server, verify images  
**Validation**: All images build, containers start, services communicate

### 5.5 - E2E Tests (2 hours)
**Purpose**: End-to-end testing  
**Key Tests**: Login, chat, memory, workflows, voice (if available)  
**Validation**: All critical paths tested and passing

### 5.6 - Documentation (1 hour)
**Purpose**: Architecture and API docs  
**Key Files**: architecture.md, api-reference.md, deployment.md  
**Validation**: Documentation complete and accurate

---

## MODULE-6: DEPLOYMENT (4 hours)

### 6.1 - Production Compose (2 hours)
**Purpose**: Production-ready docker-compose  
**Key Changes**: Remove dev volumes, add resource limits, health checks  
**Validation**: Prod compose starts, no dev dependencies

### 6.2 - Scripts (1 hour)
**Purpose**: Utility scripts  
**Key Scripts**: setup.sh, start-dev.sh, stop-all.sh, backup-volumes.sh  
**Validation**: All scripts execute successfully

### 6.3 - ComfyUI Polish (1 hour)
**Purpose**: Configure ComfyUI workflows  
**Key Tasks**: SDXL setup, custom workflows, API integration  
**Validation**: Image generation works via n8n

---

## MODULE-7: MULTI-AGENT (6 hours)

### 7.1 - CrewAI Setup (2 hours)
**Purpose**: Multi-agent orchestration  
**Key Components**: Agents definition, tasks, crew, tools  
**Validation**: Crew executes, agents collaborate

### 7.2 - Boss-Worker Pattern (2 hours)
**Purpose**: Hierarchical agent structure  
**Key Agents**: Boss (planner), Workers (specialists)  
**Validation**: Boss delegates, workers complete subtasks

### 7.3 - n8n Parallel Agents (2 hours)
**Purpose**: Workflow-based multi-agent  
**Key Features**: Parallel execution, result aggregation  
**Validation**: Multiple agents run concurrently, results merge

---

## 🎯 Critical Path (Minimum Viable Product)

For fastest path to working system:

1. **Foundation**: 1.1 → 1.2 → 1.4 (skip 1.3 if no second server)
2. **Middleware**: 2.1 → 2.2 → 2.3 (skip 2.4-2.6 initially)
3. **Frontend**: 4.1 → 4.6 → 4.5 → 5.1 → 5.2
4. **Testing**: 5.4

**Total MVP Time**: ~12 hours

Then add:
- Memory (2.4)
- Voice (MODULE-3)
- Workflows (2.5, 5.3)
- Multi-agent (MODULE-7)

---

## 💡 Tips

- **Commit after each station** - Easy rollback if issues
- **Test as you go** - Don't wait until the end
- **Read prompts first** - Understand before generating
- **Customize freely** - Prompts are starting points
- **Ask for help** - Use discussions for questions

---

## 🆘 Common Issues

**Docker won't start**: Check .env exists and has valid values  
**GPU not detected**: Verify NVIDIA Docker runtime installed  
**Ports in use**: Change port mappings in docker-compose.yml  
**Models not found**: Download models separately (see station docs)  
**WebSocket fails**: Check CORS_ORIGINS includes frontend URL  
**Memory errors**: Reduce MAX_CONCURRENT_SESSIONS or model size

---

**Total Course Time**: ~44 hours  
**MVP Time**: ~12 hours  
**Modules**: 7  
**Stations**: 33

*Happy Vibe Coding!* 🐈‍⬛✨
