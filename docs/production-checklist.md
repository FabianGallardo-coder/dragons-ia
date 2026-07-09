# Production Readiness Checklist

> Progreso general: **~97%**

---

## 🔴 Crítico (arreglar antes de producción)

- [x] **`render.yaml`** — Creado con web service + PostgreSQL free plan.
- [x] **`POST /game/action` sin rate limiting** — `30/min` en `/game/action`, `10/min` en `/game/new`.
- [x] **`/ready` no verifica DB** — Ahora ejecuta `SELECT 1` y retorna 503 si falla.
- [x] **`httpx` falta en `requirements.txt`** — Agregado `httpx>=0.27.0,<1.0.0`.

---

## 🟠 Alto

- [x] **Sin scripts de migración Alembic** — `initial_schema` generado con autogenerate (3 tablas). En prod corre `alembic upgrade head`; en dev usa `create_tables()`.
- [x] **Sin endpoint `PUT /characters/{id}`** — Creado con schema `CharacterEditRequest` (name, race, class, stats, etc.).
- [x] **Sin reset de contraseña** — `POST /auth/forgot-password` + `POST /auth/reset-password` con token en DB (expira 15min). En debug devuelve el token.
- [x] **docker-compose usa MySQL, prod usa PostgreSQL** — Migrado a PostgreSQL 16 Alpine.
- [x] **CORS `*` en debug** — Eliminado. En debug solo permite localhost.

---



## 📋 Immersion Engine — Roadmap

> Progreso: **Fase 0 (MVP) ✅ · Fase 1 (Beta) ✅ · Fase 2 (v1.0) 🔄**

### Fase 0 — MVP (Completada)
- [x] ASCII Registry modular: 25+ escenas × 2 variantes con selección procedural por seed
- [x] AnimationManager: partículas CSS para lluvia, nieve, niebla, brasas, polvo, hojas
- [x] AudioManager: skeleton listo para Fase 1
- [x] AssetRegistry: registro central de activos
- [x] `ImmersionEngine` integrado como orquestador único (reemplaza `displayAsciiArt()`)
- [x] UI dinámica: temas con transiciones CSS suaves, brillo ajustable por hora/luz

### Fase 1 — Beta (Completada)
- [x] ASCII modular por capas: 11 fondos × 15 elementos × 10 criaturas × 5 decoraciones
- [x] Sistema de variantes con seeded PRNG (Mulberry32) para no repetir arte
- [x] 10+ SFX sintetizados vía Web Audio API (fuego, lluvia, viento, pasos, espada, magia, puerta, agua, monstruo, campana, trueno, latido)
- [x] Sistema de ambientes ambientales: fire, wind, rain, waves, dripping, birds
- [x] UI dinámica extendida: scene-specific radial gradients, danger glow pulsante con CSS keyframes, scrollbar temática con colores dinámicos, brillo ajustable por luz/tiempo
- [x] Animaciones de transición entre escenas (fade-out → render nuevo → fade-in con async/await y transitionend)

### Fase 2 — v1.0 (En progreso)
- [x] Música procedural mejorada: progresiones de acordes por escena (19 escenas), ADSR, LFO vibrato, reverb por convolución
- [x] Transiciones crossfade de 3s entre pistas con fade-out asíncrono
- [x] Sincronización TTS con eventos de escena (anuncios automáticos por voz)
- [x] Modo cinemático: overlay fullscreen con título + ASCII + fade-in/out + música (CinematicMode.show())
- [x] Efectos visuales GLSL: 4 shaders (fuego, agua, niebla, magia) con WebGL canvas overlay
- [ ] SoundFont loader: integración con js-synthesizer para eawpats MIDI bank

---

## 🧪 Testing

| Área | Tests | Estado |
|------|-------|--------|
| Backend (pytest) | 45 | Cubre auth, saves, schemas, system_check |
| Frontend (Node) | 26 | Cubre dados, XP, estado IA |
| Immersion Engine | **0** | No hay tests para SceneAnalyzer, ThemeManager, ASCIIManager |
| Characters CRUD | **0** | No existe `test_characters.py` |
| Game flow (new/action) | **0** | No hay tests de `parse_game_data`, `_apply_game_state`, muerte |
| Dice service | **0** | No hay tests de `roll_dice`, `calculate_hp`, `roll_stats` |
| Dungeon Master prompts | **0** | No hay tests de `build_system_prompt` |
| TTS | **0** | No hay tests de Piper detection ni speech generation |
| E2E flow | 7 | Selenium test reparado (password2, redirects, login con email) |

- [ ] Crear tests para ImmersionEngine (SceneAnalyzer, ThemeManager, ASCIIManager, AnimationManager)
- [ ] Crear `test_characters.py` (CRUD)
- [ ] Crear `test_game.py` (new, action, game_data parser, death)
- [ ] Crear `test_dice.py` (roll_dice, stat_modifier, calculate_hp)
- [ ] Crear `test_dungeon_master.py` (system prompts por mundo)
- [ ] Crear `test_tts.py` (Piper status, generation)
- [ ] Test de aislamiento entre usuarios (User A no ve datos de User B)

---

## ✅ Ya implementado

- [x] Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
- [x] Rate limiting en auth (5/min, 10000/min en debug)
- [x] Retry con backoff en 502/503/504
- [x] Fallback inteligente de modelos Ollama según RAM
- [x] JWT con detección local de expiración + auto-logout
- [x] Clean code: sin TODOs/FIXMEs, docstrings completos
- [x] Integración TTS completa (Web Speech API + Piper TTS)
- [x] Docker: two-stage build, non-root user, HEALTHCHECK
- [x] CI/CD pipeline (GitHub Actions)
- [x] MIT License, CHANGELOG, CONTRIBUTING, INTEGRATIONS
- [x] Documentación: architecture.md, api.md, deployment.md, user-guide.md
- [x] Logging estructurado (JSONFormatter + legible en debug)
- [x] Tailwind self-hosted (eliminada dependencia CDN + CSP más limpia)
- [x] Archivos backup removidos (ai_service.py.backup, config.html.backup)
- [x] `get_db()` con `@asynccontextmanager` + `check_db_connection()`
- [x] Paginación en `GET /game/saves` (offset/limit)
- [x] Sentry SDK opcional (via SENTRY_DSN env var)
- [x] E2E tests reparados (password2, redirects, login con email)
