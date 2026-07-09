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

### Immersion Engine (Frontend)
The Immersion Engine is a modular frontend system that transforms the AI's structured SCENE_DATA into a full audiovisual experience.

```
ImmersionEngine (Orchestrator)
├── SceneAnalyzer      — Analiza SCENE_DATA + fallback por regex
├── ThemeManager       — Variables CSS dinámicas (colores, brillo, bordes, glow)
├── ASCIIManager       — Sistema de capas modular (11 fondos × 15 features × 10 criaturas × 5 decoraciones)
├── AnimationManager   — Partículas CSS ligeras (lluvia, nieve, niebla, brasas)
├── AudioManager       — Síntesis Web Audio API: música procedural con acordes, 12 SFX, ambientes
├── CinematicMode      — Overlay fullscreen con fade-in/out para momentos clave
├── GLSLFX             — Efectos WebGL (fuego, agua, niebla, magia) por escena/tema
├── TTSSync            — Anuncios por voz al cambiar de escena/peligro
├── SoundFontLoader    — Cargador opcional de SoundFont (eawpats FluidR3Mono.sf3)
└── AssetRegistry      — Catálogo central de todos los assets
```

**Data flow**: Backend genera `[SCENE_DATA: scene=cave, weather=none, ...]` → `_parse_scene_data()` extrae → `GameResponse.scene_data` → frontend `ImmersionEngine.update()` → cada manager aplica su capa.

### ASCII Art
- **Modular layer system**: 11 backgrounds × 15 features × 10 creatures × 5 decorations composed via character-grid overlay (non-space chars overwrite)
- **8,250+ unique combinations** via seeded PRNG (Mulberry32) — never repeat the same composition
- **No backend dependency**: all art composed client-side from `_BG`, `_FEATURES`, `_CREATURES`, `_DECORATIONS` registries
- **Scene transitions**: async fade-out (300ms CSS transition) → compose new art → fade-in
- **Rendering**: `<pre id="ascii-art-display">` with monospace font, full-width container, scrollable, with fade transitions
- **FIGlet banners**: still generated server-side via `art` library for titles

### Particle Animations
- CSS-only particles for: rain, snow, fog, embers, dust, leaves
- Uses compositor-only properties (transform, opacity) — zero layout impact
- Triggered automatically by `AnimationManager` based on scene weather/time
- Max 30 elements, auto-cleanup when scene changes

### Cinematic Mode (Phase 2)
- Full-screen overlay (`#cinematic-overlay`) with title + ASCII art centerd
- CSS transitions: title slides down (translateY), ASCII scales in (scale), overlay fades
- Orchestrated via `ImmersionEngine.showCinematic(sceneData, duration)` which returns a Promise
- Automatically plays scene music during cinematic via `AudioManager.playMusic()`
- Used for: game intros, boss encounters, major plot revelations, death/resurrection scenes

### GLSL Visual Effects (Phase 2)
- WebGL canvas overlay (`#glsl-canvas`) with 4 fragment shaders:
  - **fire**: perlin-like noise with red/orange gradient, alpha decays with height
  - **water**: sine waves with blue/teal palette, animated by uTime
  - **fog**: layered noise with gray/blue tint, fades toward bottom
  - **magic**: radial spiral with purple/blue glow, SVG-like sworl pattern
- Each shader maps to specific scenes/themes via `EFFECT_SCENE_MAP`
- WebGL context created with alpha channel for transparency
- Smooth 2s CSS opacity transition on show/hide
- Falls back to `prefers-reduced-motion: reduce` (hidden)

### Audio (Phase 1 — Implemented, Enhanced in Phase 2)
- **SFX**: 12 synthesized effects via Web Audio API — zero sample files:
  - `fire` — noise + lowpass filter with crackling
  - `rain` — highpass noise burst droplets
  - `wind` — filtered noise sweeping 200→2000Hz
  - `footsteps` — low-frequency thump triplets
  - `sword` — bandpass noise burst + sine ring (800Hz)
  - `magic` — arpeggio (6 notes, 400→1200Hz)
  - `door` — sawtooth sweep 200→80Hz
  - `water` — randomized sine plops
  - `monster` — lowpass sawtooth growl 40→80Hz
  - `bell` — 4-harmonic chime (440Hz fundamental)
  - `thunder` — noise burst with lowpass decay
  - `heartbeat` — paired low-frequency thumps
- **Ambience System**: looping background textures (fire, wind, rain, waves, dripping, birds) with independent gain staging
- **Music**: enhanced procedural system with 19 scene-specific chord progressions (e.g., tavern: C-D-E-D, dungeon: C3-G3-C4-G3), ADSR envelopes per note, LFO vibrato, and convolution reverb (2s impulse response)
- **Crossfade**: 3s `linearRampToValueAtTime` to 0 → stop old → start new → ramp to target gain
- **Architecture**: three independent gain nodes (musicGain, ambienceGain, sfxGain) under masterGain for independent volume control
- **Trigger API**: `AudioManager.trigger(event)` maps game events (hit, magic, death, victory, door, etc.) to SFX

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
