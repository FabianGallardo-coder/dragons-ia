# Integrations

## AI Providers

### Anthropic (Claude)
- API Key authentication
- Models: claude-3-5-haiku-20241022 (example)
- Configuration via frontend → Settings → Anthropic

### Ollama Cloud
- API Key authentication
- Models: gemma3:4b, gemma3:12b, gemma3:27b, ministral-3:8b, deepseek-v3.1:671b, qwen3.5:397b
- Configuration via frontend → Settings → Ollama Cloud

### Ollama Local
- No API key required (runs locally)
- Models: dolphin-mistral:7b-v2.6-dpo-laser-q4_K_M, dolphin-phi
- Configuration via frontend → Settings → Ollama Local

## Text-to-Speech (TTS)

### Web Speech API
- Browser-native speech synthesis
- Free, no additional setup
- Available in Chrome, Edge, Safari

### Piper TTS (Docker)
- Higher quality voice synthesis
- HTTP server at `piper_server/main.py` (endpoints: `/health`, `/synthesize`)
- Docker service with `--profile tts` in docker-compose
- Model: `es_MX/claude/high/es_MX-claude-high`
- Volume mount: `./piper_voices/`
- Fallback: Web Speech API if Piper unavailable

### TTS Filtering
- Backend: `_clean_for_tts()` removes GAME_DATA/SCENE_DATA, thinking tags, metadata, URLs, markdown
- Schema: `narrative_tts` field in `GameResponse`
- Frontend: `_cleanText()` strips HTML, code blocks, URLs before speaking

## SoundFont (Music)
- SoundFontLoader in `frontend/static/js/immersion/soundfont_loader.js`
- MIDI playback via Web Audio API (eawpats)
- Integrated in AudioManager: scene-dependent chord progressions
- 19 scene-to-progression mappings

## Deployment & Infrastructure

### Render.com
- Primary deployment platform
- Uses render.yaml for automatic configuration
- Environment variables: DATABASE_URL, JWT_SECRET_KEY, DEBUG, TTS_ENABLED, TTS_URL

### Docker
- Dockerfile (Python 3.12-slim, multi-stage build)
- docker-compose.yml with profiles: default, tts, full
- piper_server/ has its own Dockerfile
- Image: dragons-ia
- Healthcheck: HTTP GET /health
- Database: PostgreSQL (prod) / SQLite (dev)

## Authentication & Security

### JWT Authentication
- python-jose library
- 24-hour token expiration
- Auto-logout on token expiration
- Local storage of tokens (never sent to server)

### Rate Limiting
- slowapi: 100 requests/minute
- Automatically disabled during tests (monkey-patch)

## Testing

### Backend
- pytest with pytest-asyncio
- 123/129 tests passing (6 selenium skipped)
- Tests: schemas (15), auth (11), saves (10), characters (10), dice (16), game (19), dungeon_master (20), tts (6), user_isolation (4), ai_service (3), system_check (6)

### Frontend
- Node.js stdlib for testing game logic
- 18 immersion engine tests (ASCII, particles, audio, GLSL, themes)

## Monitoring & Diagnostics

### Ollama Status Detection
- Endpoint: GET /api/system/ollama-status
- Real-time frontend diagnostics in config.html
- Automatic fallback when models not installed
- RAM-based model recommendations

## Immersion Engine

### Components
- SceneAnalyzer — parses SCENE_DATA + regex fallback
- ThemeManager — dynamic CSS variables
- ASCIIManager — 25+ modular scenes, 10,000+ combinations
- AnimationManager — CSS particles (rain, snow, fog, embers, dust, leaves)
- AudioManager — Web Audio API SFX + music (SoundFont)
- CinematicMode — fullscreen overlay with title + ASCII + music
- GLSL effects — WebGL fire, water, fog, magic shaders
- TTSSync — voice announcements on scene transitions
- AssetRegistry — central asset catalog
