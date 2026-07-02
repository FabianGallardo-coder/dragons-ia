# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- TTS Narración por voz: Web Speech API + Piper TTS local
- `frontend/static/js/tts.js` — módulo TTS con detección automática de Piper
- `backend/services/tts_service.py` — servicio Piper TTS con modelo es_MX-claude-high
- `backend/routers/tts.py` — endpoint `GET /api/tts/status` y `POST /api/tts`
- UI de control TTS en `game.html` (toggle, velocidad) y `config.html` (voz, velocidad)
- Integración automática: la narración del DM se reproduce por voz
- Modelos de Ollama Cloud cargados dinámicamente desde la API oficial
- Endpoint `POST /game/ollama/models/cloud` — obtiene modelos disponibles según API key
- Prewarm de TTS por gesto del usuario (click/keydown/touchstart) para Chrome
- `media-src 'self' blob:` en CSP header para permitir blob URLs de audio

### Changed
- `requirements.txt` — limpiado (encoding UTF-8), agregado piper-tts
- `backend/main.py` — registrado router TTS
- `backend/database.py:get_db()` — `@asynccontextmanager` reemplazado por `async def` con `yield`
- `backend/services/system_check.py` — usa `settings.ollama_api_base` en lugar de URL hardcodeada
- `backend/services/tts_service.py` — `--output-raw` eliminado, Piper genera WAV válido
- `game.js:applyWorldFont()` — fuente Cinzel aplicada solo a `#narrative-container`, controles en Inter
- `docker-compose.yml` — agregado `OLLAMA_API_BASE`, `extra_hosts: ["host.docker.internal:host-gateway"]`
- `.dockerignore` — solo excluye `frontend/node_modules/`, ya no excluye HTML
- `config.html` — modelos dinámicos vía API, `showToast` reemplazado por `showMsg`
- Layout de `game.html` — ASCII art ocupa todo el ancho disponible (sin `max-w-4xl`)

### Fixed
- `@asynccontextmanager` en dependencia FastAPI causaba `TypeError: '_AsyncGeneratorContextManager' object is not an async iterator`
- Piper TTS devolvía `--output-raw` sin cabecera WAV → `NotSupportedError` en Chrome
- `audio.play()` sin `.catch()` en `_speakPiper()` → promesa rechazada no capturada, sin fallback a Web Speech
- Chrome bloqueaba `speechSynthesis.speak()` en callbacks async sin gesto de usuario
- CSP bloqueaba `blob:` URLs para audio (`media-src` no estaba configurado)
- Modelo `rnj-1:8b` no existe en Ollama Cloud (eliminado de la lista hardcodeada)

## [1.1.0] - 2026-07-01
### Added
- Ollama system detection module: `backend/services/system_check.py`
- Endpoint `GET /api/system/ollama-status` con diagnóstico en tiempo real
- Frontend diagnostics banner en `config.html` (verde/amarillo/rojo)
- Fallback inteligente de modelos en `ai_service.py`
- DM immersion rules y tono diferenciado por mundo
- Fuentes tipográficas temáticas por mundo (Cinzel, Orbitron, Philosopher, Crimson Text)
- Rate limiting con slowapi (100 req/min)
- Security headers middleware (HSTS, CSP, X-Frame-Options, etc.)

### Changed
- README actualizado con documentación de Ollama system detection
- Mejora en UI: HP/XP bars, dados con crítico/pifia, indicador de estado IA
- Auto-logout con detección local de token expirado
- Retry automático con backoff en errores 502/503/504

### Fixed
- Validación de modelo IA en localStorage para evitar valores basura
- Layout h-screen: HP/XP/status siempre visibles en footer

## [1.0.0] - 2026-06-30
### Added
- Initial release of Dragons & IA game
- Character creation with D&D 5e stats (Point Buy)
- AI Dungeon Master integration via LiteLLM
- Multiple world support: Fantasía Medieval, Ciencia Ficción, Isekai, Fantasía Oscura
- Interactive dice rolling (d4-d20)
- Save/load game system
- JWT authentication (24h expiration)
- Multiple AI providers: Anthropic, Ollama Cloud, Ollama Local
- Responsive UI with Tailwind CSS
- Docker deployment support
