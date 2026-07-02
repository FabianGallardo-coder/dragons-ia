# System Architecture

## Overview
Dragons & IA is a text-based RPG powered by AI that acts as a Dungeon Master. Players create characters, choose worlds, and experience adventures narrated in real-time by artificial intelligence.

## Components

### Backend (FastAPI + Python 3.11+)
- **Entry point**: `backend/main.py` — FastAPI app with CORS, security headers, rate limiting
- **Config**: `backend/config.py` — Pydantic Settings from `.env`
- **Database**: `backend/database.py` — SQLAlchemy 2.0 async engine
- **Models**: `backend/models/` — ORM: User, Character, SaveGame
- **Routers**: `backend/routers/` — auth, characters, game, system, tts
- **Services**: `backend/services/` — ai_service, dungeon_master, dice, system_check, tts_service

### Database
- **Production**: PostgreSQL via asyncpg
- **Development**: SQLite via aiosqlite
- **ORM**: SQLAlchemy 2.0 async with Alembic migrations
- **Auto-migration**: Tables created on startup via `create_tables()`

### Frontend (HTML5 + Tailwind CSS + Vanilla JS)
- **Pages**: index, login, register, world, character, confirm, game, config
- **JS modules**: api.js (fetch + retry), auth.js (JWT + localStorage), game.js (game logic), tts.js (voice narration)
- **No framework**: vanilla JS for zero build step

### AI Services (LiteLLM)
- **Anthropic Claude**: API key stored in browser localStorage
- **Ollama Cloud**: API key stored in browser localStorage
- **Ollama Local**: No API key, runs on user's machine
- **Fallback**: Auto-detects available models and selects best fit for RAM

### TTS (Text-to-Speech)
- **Primary**: Web Speech API (browser-native, no backend needed, with user-gesture prewarm for Chrome)
- **Upgrade**: Piper TTS local (via `POST /api/tts`) with es_MX-claude-high voice model
- **Auto-detection**: Frontend fetches `GET /api/tts/status` and enables Piper mode if available + voice exists
- **Fallback**: If Piper playback fails (`audio.play()` rejection), falls back to Web Speech API automatically
- **Format**: Piper outputs valid WAV (sin cabecera se eliminó `--output-raw` en `tts_service.py`)
- **CSP**: `media-src 'self' blob:` permite reproducción de audio desde blob URLs

### ASCII Art
- **Static templates**: 24 hand-crafted pieces (4 worlds × 6 events: new_game, battle, victory, death, rest, scene)
- **Selection**: Client-side `_detectEvent()` regex matches keywords in AI narrative
- **Rendering**: `<pre id="ascii-art-display">` with monospace font, full-width container, scrollable
- **Generation**: FIGlet banner via `art` library + hardcoded art from `WORLD_ART` dictionary
- **Endpoint**: `GET /api/ascii/art?world=...&event=...`

### Security Headers
- CSP: `default-src 'self'`, `script-src 'self' 'unsafe-inline'`, `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com`, `font-src 'self' https://fonts.gstatic.com`, `img-src 'self' data:`, `media-src 'self' blob:`, `connect-src 'self' https://ollama.com`
- HSTS in production only
- X-Frame-Options, X-Content-Type-Options

## Data Flow
1. User authenticates → JWT stored in localStorage
2. User creates character → POST /characters/ → stored in DB
3. User starts game → POST /game/new → AI generates opening scene
4. User sends action → POST /game/action → AI responds → narrative rendered → TTS speaks
5. Dice rolls sent with actions, HP/XP updated in real-time
6. ASCII art updated based on event type detected from AI narrative
7. Game state saved automatically on each action

## Security
- JWT with 24h expiration, verified locally and server-side
- CSP headers (`media-src 'self' blob:` for TTS audio), HSTS, X-Frame-Options, X-Content-Type-Options
- Rate limiting: 100 requests/minute via slowapi
- CORS restricted to known origins in production
- API keys never sent to server (browser → AI provider directly)
