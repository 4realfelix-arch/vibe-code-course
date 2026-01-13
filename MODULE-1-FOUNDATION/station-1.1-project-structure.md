# Station 1.1 - Project Structure Setup

## Overview
Set up the complete directory structure for Atomic Cat AI, a multi-service AI voice assistant with Docker Compose orchestration. This station establishes the foundation for all subsequent modules.

## Learning Objectives
- Understand monorepo structure for multi-service applications
- Learn proper file organization for Docker-based projects
- Set up version control with appropriate gitignore rules
- Create comprehensive project documentation

---

## 🎯 GENERATION PROMPT

Create a complete project directory structure for "Atomic Cat AI" - a multi-user AI voice assistant with the following requirements:

**Project Name**: atomic-cat-ai

**Directory Structure**:
```
atomic-cat-ai/
├── README.md                      # Project overview with quick start
├── .gitignore                     # Exclude build artifacts, dependencies, secrets
├── .env.example                   # Template for environment variables
├── docker-compose.yml             # Server 1: Core services
├── docker-compose.server2.yml     # Server 2: GPU workloads
├── middleware/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── auth.py                    # Authentication and proxy
│   ├── chat.py                    # Chat endpoint with memory
│   ├── voice_websocket.py         # Voice WebSocket handler
│   ├── workflow_service.py        # n8n workflow triggers
│   ├── memory_client.py           # Mem0 integration
│   ├── config.py                  # Configuration management
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Middleware container
├── frontend/
│   ├── package.json               # Node.js dependencies
│   ├── svelte.config.js           # SvelteKit configuration
│   ├── vite.config.ts             # Vite build configuration
│   ├── tailwind.config.js         # Tailwind CSS configuration
│   ├── tsconfig.json              # TypeScript configuration
│   ├── src/
│   │   ├── app.html               # HTML template
│   │   ├── app.css                # Global styles with atomic theme
│   │   ├── routes/
│   │   │   ├── +layout.svelte     # Root layout
│   │   │   ├── +page.svelte       # Main chat page
│   │   │   └── login/
│   │   │       └── +page.svelte   # Login page
│   │   ├── lib/
│   │   │   ├── stores/
│   │   │   │   ├── chat.ts        # Chat state management
│   │   │   │   ├── auth.ts        # Auth state
│   │   │   │   └── websocket.ts   # WebSocket connection
│   │   │   ├── components/
│   │   │   │   ├── CatAvatar.svelte      # Animated cat mascot
│   │   │   │   ├── ChatInput.svelte      # Message input
│   │   │   │   ├── ChatMessages.svelte   # Message list
│   │   │   │   ├── Sidebar.svelte        # Conversation history
│   │   │   │   └── DetailsPanel.svelte   # User info panel
│   │   │   ├── api/
│   │   │   │   └── client.ts      # API client wrapper
│   │   │   └── types/
│   │   │       └── index.ts       # TypeScript interfaces
│   │   └── static/
│   │       └── favicon.png        # Cat icon
│   └── Dockerfile                 # Frontend container
├── voice-server/
│   ├── server.py                  # Python voice processing server
│   ├── vad.py                     # Voice Activity Detection
│   ├── audio_processor.py         # Audio stream processing
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Voice server container
├── workflows/
│   ├── image-generation.json      # n8n workflow for ComfyUI
│   ├── memory-search.json         # n8n workflow for memory queries
│   └── multi-agent-crew.json      # n8n workflow for CrewAI
├── scripts/
│   ├── setup.sh                   # Initial setup script
│   ├── start-dev.sh               # Development startup
│   ├── stop-all.sh                # Stop all services
│   └── backup-volumes.sh          # Backup Docker volumes
├── tests/
│   ├── test_middleware.py         # FastAPI tests
│   ├── test_voice.py              # Voice server tests
│   └── test_e2e.py                # End-to-end tests
└── docs/
    ├── architecture.md            # System architecture
    ├── api-reference.md           # API documentation
    └── deployment.md              # Deployment guide
```

**Requirements**:
1. Create all directories with proper nesting
2. Create empty `__init__.py` files in Python packages
3. Create `.gitignore` that excludes:
   - `node_modules/`, `__pycache__/`, `*.pyc`, `.venv/`, `venv/`
   - `.env` (but NOT `.env.example`)
   - `*.log`, `*.tmp`
   - `models/`, `downloads/`, `uploads/`
   - `.DS_Store`, `Thumbs.db`
   - `dist/`, `build/`, `.svelte-kit/`
4. Create `README.md` with:
   - ASCII cat banner
   - "Atomic Cat AI" title with atomic emoji ⚛️🐈‍⬛
   - Brief description
   - Prerequisites section (Docker, Docker Compose, GPU optional)
   - Quick start instructions (5 steps)
   - Architecture diagram (ASCII art acceptable)
   - Tech stack list
   - Links to documentation
5. All files should be created, even if initially empty (except .gitignore and README.md which should be complete)

**Output**: Generate the complete command sequence (mkdir, touch, echo) to create this structure, then show the tree structure to verify.

---

## ✅ VALIDATION PROMPT

Verify the project structure meets these requirements:

### Directory Structure Validation
- [ ] All top-level directories exist: `middleware/`, `frontend/`, `voice-server/`, `workflows/`, `scripts/`, `tests/`, `docs/`
- [ ] Frontend has proper SvelteKit structure: `src/routes/`, `src/lib/`, `src/static/`
- [ ] Middleware has all required Python modules
- [ ] All Python packages have `__init__.py` files

### Git Configuration
- [ ] `.gitignore` exists and excludes:
  - `node_modules/` and `__pycache__/`
  - Virtual environments (`venv/`, `.venv/`)
  - Environment files (`.env` but NOT `.env.example`)
  - Build artifacts (`dist/`, `build/`, `.svelte-kit/`)
  - Model files (`models/`)
  - Log files (`*.log`)
- [ ] `.gitignore` does NOT exclude:
  - `Dockerfile` files
  - `.env.example`
  - Source code files

### README.md Validation
- [ ] Contains ASCII art cat banner or emoji
- [ ] Has "Atomic Cat AI" as main title
- [ ] Includes prerequisites section with:
  - Docker & Docker Compose version requirements
  - RAM requirements (16GB+)
  - GPU requirements (optional but recommended)
  - Disk space requirements (50GB+)
- [ ] Has quick start section with exact 5 steps:
  1. Clone repository
  2. Copy `.env.example` to `.env`
  3. Start Server 1 services
  4. (Optional) Start Server 2 services
  5. Access URLs
- [ ] Lists all major technologies:
  - Backend: Open WebUI, Ollama, FastAPI
  - Frontend: SvelteKit, Tailwind CSS
  - Voice: LFM2.5-Audio-1.5B
  - Images: ComfyUI + SDXL
  - Memory: Mem0, Qdrant
  - Workflows: n8n
  - Multi-Agent: CrewAI

### Best Practices
- [ ] Follows monorepo structure with clear service separation
- [ ] Uses consistent naming (kebab-case for directories)
- [ ] Includes Dockerfile in each service directory
- [ ] Has dedicated directories for tests and documentation
- [ ] Scripts directory contains utility shell scripts

### Commands to Run
```bash
# Verify directory structure
tree -L 3 -a

# Check .gitignore excludes correct files
cat .gitignore

# Verify README has all required sections
cat README.md | grep -E "Prerequisites|Quick Start|Tech Stack"

# Count files created
find . -type f | wc -l
# Should have 20+ files

# Verify Python __init__.py files
find middleware -name "__init__.py"
```

### Expected Results
- All directories and files exist
- `.gitignore` properly configured
- README.md is comprehensive and helpful
- Project structure follows monorepo best practices
- Ready for next station (Docker Compose setup)

---

## Notes
- This station focuses on structure only, not implementation
- Empty files are acceptable at this stage
- Next station will populate Docker Compose configurations
- Commit this structure before proceeding to Station 1.2
