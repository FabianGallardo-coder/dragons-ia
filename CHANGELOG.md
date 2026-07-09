# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- TTS opcional vía Docker: nuevo servicio `piper-tts` con profile, env vars `TTS_ENABLED`, `TTS_URL`, `TTS_VOICE`
- TTS dual-mode: soporte HTTP (Docker) y subprocess (local) con detección automática
- Health check en `docker-compose.yml` para `app` + `postgres`
- Tests de backend: characters (CRUD, 18), dice (15), game (21), dungeon_master (20), tts (6), user_isolation (6)
- Tests de frontend: 18 tests de inmersión visual (ASCII, partículas, audio, GLSL, temas)
- Rate limiter deshabilitado automáticamente en tests mediante monkey-patch de slowapi

### Changed
- `docker-compose.yml`: Piper como servicio opcional (profile `tts`/`full`), healthcheck en app
- `backend/services/tts_service.py`: refactor completo con soporte HTTP (`TTS_URL`) + subprocess
- `tests/conftest.py`: deshabilitado rate limiting para tests vía monkey-patch temprano de slowapi
- `.env.example`: nuevas vars `TTS_ENABLED`, `TTS_URL`, `TTS_VOICE`

### Fixed
- Tests de autenticación: status code corregido de 403→401 (coincide con la implementación real)
- Tests de saves: status code corregido de 403→401
- Tests de dice: stat modifier corregido (stat 1 → -5 según D&D 5e)

### Removed
- Directorios vacíos `worktrees/` y `.claude/worktrees/`
- Caches de pytest y Python eliminados

### Added — Immersion Engine Phase 0 (MVP) + Phase 1 (Beta)
- `frontend/static/js/immersion/ascii_manager.js` — ASCII Registry modular: 25+ escenas × 2 variantes con selección por seed (10,000+ combinaciones por capas)
- `frontend/static/js/immersion/animation_manager.js` — Partículas CSS ligeras: lluvia, nieve, niebla, brasas, polvo, hojas
- `frontend/static/js/immersion/audio_manager.js` — SFX procedural completo: 12 efectos sintetizados vía Web Audio API (fuego, lluvia, viento, pasos, espada, magia, puerta, agua, monstruo, campana, trueno, latido) + sistema de ambientes (fuego, viento, lluvia, olas, dripping, pájaros)
- `frontend/static/js/immersion/asset_registry.js` — Registro central de assets (texturas, animaciones, sonidos)
- ASCII modular por capas: 11 fondos × 15 elementos × 10 criaturas × 5 decoraciones (8,250+ combinaciones)
- Sistema de seeded PRNG (Mulberry32) para variantes sin repetición
- Transiciones de escena: fade-out del ASCII anterior → render nuevo → fade-in con CSS transitions
- Efecto danger glow pulsante en ASCII container durante combate/boss
- Scene-specific background radial gradients vía `--theme-scene-bg`
- Música procedural mejorada: progresiones de acordes por escena (19 mapeos), ADSR, LFO vibrato, reverb por convolución
- Crossfade de 3s entre pistas musicales con fade-out asíncrono vía `_crossfadeMusic()`
- `frontend/static/js/immersion/cinematic_mode.js` — Modo cinemático: overlay fullscreen con título + ASCII + fade-in/out + música
- `frontend/static/js/immersion/glsl_effects.js` — Efectos GLSL vía WebGL: fuego, agua, niebla, magia (4 fragment shaders con uniformes uTime/uRes)
- `frontend/static/js/immersion/tts_sync.js` — Sincronización TTS con eventos de escena (anuncios por voz al cambiar de escena/peligro)
- `ImmersionEngine` completamente integrado: orquesta ASCII + Animaciones + Tema + Audio
- UI dinámica extendida: background gradients, border glow, brightness por hora/luz
- Animaciones CSS de partículas con `content-visibility` y compositor-only para máximo rendimiento

### Changed
- Sistema ASCII rediseñado: de 24 piezas fijas (4 mundos × 6 eventos) a 25+ escenas modulares con variantes
- `ImmersionEngine.update()` ahora reemplaza completamente `displayAsciiArt()` como sistema único
- `game.js:displayAsciiArt()` — eliminada en favor del nuevo ASCIIManager local (sin llamadas al backend)
- `game.html` — nuevos script tags para los módulos del immersion engine
- `style.css` — animaciones de partículas, transiciones de escena, variables CSS extendidas
- `engine.js` — eliminados TODOs de AnimationManager y AudioManager

### Fixed
- Dependencia del backend para ASCII art eliminada: todo el arte se sirve desde el frontend
- `_detectEvent()` reemplazado por `SceneAnalyzer` con datos estructurados del SCENE_DATA

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
