# OpenWiki Quickstart

This document serves as the entry point for understanding the Dragons-IA project.

## Overview

Dragons-IA is a text-based RPG with an AI-powered Dungeon Master. Players create D&D 5e characters, choose a world, and interact with an AI that narrates adventures, manages game state, and responds to player actions.

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic
- **Frontend:** HTML5, Tailwind CSS, vanilla JavaScript (ES modules)
- **Database:** PostgreSQL (production), SQLite (development)
- **AI:** LiteLLM (Ollama local/cloud, Anthropic Claude)
- **TTS:** Piper TTS (Docker) + Web Speech API (browser fallback)
- **Deployment:** Docker multi-stage build, Render.com

## Quick Start

```bash
# Clone and setup
git clone https://github.com/FrancoStino/dragons-ia.git
cd dragons-ia
cp .env.example .env

# Local (no Docker)
pip install -r requirements.txt
uvicorn backend.main:app --reload

# With Docker
docker compose up --build
```

## Architecture

```
frontend/          → HTML + CSS + JS (static files served by FastAPI)
backend/
  main.py          → FastAPI app, middleware, routers
  config.py        → Pydantic Settings (env-based)
  database.py      → SQLAlchemy async engine
  routers/         → HTTP endpoints (auth, game, characters, tts, ascii_art, system)
  services/        → Business logic (ai_service, dungeon_master, dice, tts, ascii_art, system_check)
  models/          → ORM models (User, Character, SaveGame, ResetToken)
  schemas/         → Pydantic request/response schemas
  alembic/         → Database migrations
tests/             → pytest + Node.js tests
piper_server/      → Standalone Piper TTS HTTP server
```

## Key Concepts

### Game Flow
1. Register/Login → JWT token
2. Choose world (Fantasia, Sci-Fi, Isekai, Dark Fantasy)
3. Create character (D&D 5e point buy stats)
4. Start game → AI generates opening scene
5. Send actions → AI narrates responses with GAME_DATA (HP/XP changes) and SCENE_DATA (visual/audio metadata)

### Immersion Engine
Frontend modules that react to SCENE_DATA:
- **ThemeManager** — Dynamic CSS variables per scene
- **ASCIIManager** — 8,250+ modular ASCII art combinations
- **AudioManager** — Procedural music + SFX via Web Audio API
- **AnimationManager** — CSS particle effects (rain, snow, fog)
- **GLSLFX** — WebGL fragment shaders
- **CinematicMode** — Fullscreen overlay for scene transitions
- **TTSSync** — Voice announcements on scene changes

### AI Integration
- **Dungeon Master** — System prompt with 4 immersion rules, 10 narration rules, per-world tone
- **GAME_DATA** — Structured output: `[GAME_DATA: hp_change=X, xp_gain=Y, alive=true/false]`
- **SCENE_DATA** — Visual metadata: `[SCENE_DATA: scene=X, weather=X, time=X, ...]`

## API Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/auth/register` | No | Register user |
| POST | `/auth/login` | No | Login |
| POST | `/auth/forgot-password` | No | Request password reset |
| POST | `/auth/reset-password` | No | Reset password with token |
| GET | `/auth/me` | Yes | Get current user |
| POST | `/characters/` | Yes | Create character |
| GET | `/characters/` | Yes | List characters |
| POST | `/game/new` | Yes | Start new game |
| POST | `/game/action` | Yes | Send player action |
| GET | `/game/saves` | Yes | List save games |
| GET | `/api/tts/status` | No | TTS availability |
| POST | `/api/tts` | No | Generate speech audio |
| GET | `/api/ascii/art` | No | ASCII art banner |
| GET | `/api/system/ollama-status` | No | Ollama diagnostics |
| GET | `/health` | No | Liveness check |
| GET | `/ready` | No | Readiness check |

## Running Tests

```bash
# Backend (pytest)
pytest -v

# Frontend (Node.js)
node tests/frontend/test_game_logic.js
node tests/frontend/test_immersion_engine.js
```

## Environment Variables

See `.env.example` for all configuration options. Key variables:
- `DATABASE_URL` — PostgreSQL connection string
- `JWT_SECRET_KEY` — Min 32 chars, required in production
- `DEFAULT_AI_MODEL` — Ollama model identifier
- `OLLAMA_API_BASE` — Ollama server URL
- `TTS_ENABLED` / `TTS_URL` — Piper TTS configuration
- `CORS_ORIGINS` — Comma-separated allowed origins
- `SENTRY_DSN` — Optional error tracking

## Documentation

- [Architecture](architecture.md)
- [Data Models & Storage](data_models_storage.md)
- [Workflows & Features](workflows_features.md)
- [Testing & Integrations](testing_integrations.md)
- [Deployment & Operations](deployment_operations.md)

---

_Generated and maintained by OpenWiki._
