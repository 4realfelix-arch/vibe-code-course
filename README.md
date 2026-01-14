# 🐈‍⬛ Atomic Cat AI - Vibe Code Course

```
     /\_/\
    ( o.o )    ╔═══════════════════════════════════════════╗
     > ^ <     ║  ATOMIC CAT AI: VIBE CODE CURRICULUM      ║
    /|   |\    ║  Learn to Build AI Voice Assistants       ║
   (_|   |_)   ║  with Multi-Agent Intelligence            ║
                ╚═══════════════════════════════════════════╝
    ★ ✦ ★ ✧ ★ ✦ ★ R E T R O - F U T U R I S T I C ★ ✦ ★ ✧ ★ ✦ ★
```

## 🎯 What You'll Build

**Atomic Cat AI** - A sophisticated multi-user AI voice assistant with:
- 🗣️ Real-time voice conversations with barge-in support
- 🧠 Persistent memory across conversations
- 🎨 AI image generation with ComfyUI
- 🔄 Automated workflows with n8n
- 👥 Multi-agent orchestration with CrewAI
- 🎭 Retro 1940s atomic-era UI with animated cat avatar

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         SERVER 1                                 │
│  ┌──────────────┐  ┌──────────┐  ┌────────┐  ┌──────────────┐ │
│  │  SvelteKit   │→ │ FastAPI  │→ │  Open  │→ │    Ollama    │ │
│  │   Frontend   │  │Middleware│  │ WebUI  │  │  (llama.cpp) │ │
│  │  Port 5173   │  │Port 8000 │  │Port3000│  │  Port 11434  │ │
│  └──────────────┘  └────┬─────┘  └────────┘  └──────────────┘ │
│         ↕              ↕│↕                                      │
│  ┌──────────────┐  ┌───┴──┐  ┌─────────┐  ┌────────────────┐ │
│  │ WebSocket Hub│  │ Redis│  │ Qdrant  │  │      n8n       │ │
│  │              │  │      │  │ Vector  │  │   Workflows    │ │
│  │              │  │      │  │   DB    │  │   Port 5678    │ │
│  └──────────────┘  └──────┘  └─────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               ↕ Network ↕
┌─────────────────────────────────────────────────────────────────┐
│                         SERVER 2 (Optional GPU)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐│
│  │   ComfyUI    │  │ Voice Server │  │       Mem0/OpenMemory  ││
│  │    SDXL      │  │LFM2.5 Audio  │  │    Memory Service      ││
│  │  Port 8188   │  │ Port 8765    │  │                        ││
│  └──────────────┘  └──────────────┘  └────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (v2.0+)
- GPU with CUDA support (optional but recommended)
- 16GB+ RAM (32GB+ for full stack)
- 50GB+ disk space for models

### Setup in 5 Steps

```bash
# 1. Clone the repository
git clone https://github.com/4realfelix-arch/vibe-code-course.git
cd vibe-code-course

# 2. Copy environment template
cp TEMPLATES/.env.example .env
# Edit .env with your settings

# 3. Start core services (Server 1)
docker compose -f TEMPLATES/docker-compose.yml up -d

# 4. (Optional) Start GPU services (Server 2)
docker compose -f TEMPLATES/docker-compose.server2.yml up -d

# 5. Access the application
# Frontend: http://localhost:5173
# Open WebUI: http://localhost:3000
# n8n: http://localhost:5678
```

## 📚 Learning Path - 30 Stations Across 7 Modules

| Module | Stations | Focus Area | Duration |
|--------|----------|-----------|----------|
| **MODULE-1** | 4 | Foundation & Docker Setup | 4 hours |
| **MODULE-2** | 6 | FastAPI Middleware & Services | 8 hours |
| **MODULE-3** | 3 | Voice Processing & WebSockets | 4 hours |
| **MODULE-4** | 8 | SvelteKit Frontend & UI | 10 hours |
| **MODULE-5** | 6 | Integration & Testing | 8 hours |
| **MODULE-6** | 3 | Production Deployment | 4 hours |
| **MODULE-7** | 3 | Multi-Agent Orchestration | 6 hours |
| **Total** | **33** | **Complete Course** | **44 hours** |

### 🎓 Vibe Code Learning Method

This course uses **"Vibe Coding"** - a modern AI-assisted development approach:

1. **Generate** - Use AI to create code from detailed prompts
2. **Validate** - Run automated checks and understand what was built
3. **Iterate** - Refine and customize to your needs
4. **Learn** - Understand patterns through doing, not just reading

See [STUDENT-GUIDE.md](STUDENT-GUIDE.md) for detailed instructions on how to effectively use this method.

## 🎨 Design System - Atomic Era Theme

Our UI follows a retro-futuristic 1940s aesthetic:

| Element | Specification |
|---------|--------------|
| **Primary Colors** | Teal `#40E0D0`, Coral `#FF6F61`, Mustard `#FFD700` |
| **Accent Colors** | Mint `#98FF98`, Cream `#FFFDD0`, Charcoal `#36454F` |
| **Mascot** | 1940s black cat with yellow almond eyes, coral choker |
| **Typography** | Pacifico (display), Quicksand (body) |
| **Style** | Googie architecture with starbursts and atomic symbols |

## 🛠️ Tech Stack

### Backend & AI
- **Open WebUI** - Chat interface and model management
- **Ollama / llama.cpp** - Local LLM inference
- **FastAPI** - Python middleware and API gateway
- **Mem0 / OpenMemory MCP** - Persistent conversation memory
- **Qdrant** - Vector database for embeddings

### Orchestration & Automation
- **n8n** - Visual workflow automation
- **CrewAI** - Multi-agent orchestration framework
- **Redis** - Caching and pub/sub messaging

### Voice & Media
- **LFM2.5-Audio-1.5B** - Speech-to-Text and Text-to-Speech
- **ComfyUI + SDXL** - AI image generation pipeline

### Frontend
- **SvelteKit** - Modern reactive framework
- **Tailwind CSS** - Utility-first styling
- **WebSocket** - Real-time bidirectional communication

## 📖 Course Materials

### Station Files
Each station includes:
- 🎯 **Generation Prompt** - Give this to your AI assistant to create code
- ✅ **Validation Prompt** - Use this to verify the implementation works
- 📝 Learning objectives and context

### Support Files
- **TEMPLATES/** - Working Docker Compose configs and examples
- **CHEATSHEETS/** - Quick references and troubleshooting guides
- **example-code/** - Reference implementations

## 🎯 Learning Objectives

By completing this course, you will:

1. ✅ Deploy multi-container AI applications with Docker
2. ✅ Build production-ready FastAPI middleware services
3. ✅ Implement real-time voice processing with WebSockets
4. ✅ Create modern responsive UIs with SvelteKit
5. ✅ Integrate vector databases and memory systems
6. ✅ Orchestrate multi-agent AI workflows
7. ✅ Deploy and scale AI applications
8. ✅ Master AI-assisted development (vibe coding)

## 🤝 Contributing

This is a living curriculum! Contributions are welcome:
- Submit issues for bugs or unclear instructions
- Create PRs to improve station content
- Share your completed projects

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🆘 Need Help?

- Check [CHEATSHEETS/troubleshooting.md](CHEATSHEETS/troubleshooting.md)
- Review [CHEATSHEETS/prompt-station-quickref.md](CHEATSHEETS/prompt-station-quickref.md)
- Open an issue with the `question` label

---

<div align="center">

**Ready to build something amazing?** 🚀

Start with [MODULE-1-FOUNDATION/station-1.1-project-structure.md](MODULE-1-FOUNDATION/station-1.1-project-structure.md)

Made with ❤️ and ☕ in the spirit of 1940s atomic optimism

★ ✦ ★ ✧ ★ Happy Vibe Coding! ★ ✧ ★ ✦ ★

</div>