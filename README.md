# ⚔️ Dragons & IA

> Juego de rol por texto impulsado por Inteligencia Artificial que actúa como Dungeon Master.

El jugador crea un personaje, elige un mundo y vive una aventura narrada en tiempo real por una IA.
Soporta múltiples modelos de IA: Anthropic (Claude), Ollama Cloud y modelos locales vía Ollama.

🔗 **Demo en vivo:** [dragons-ia.onrender.com](https://dragons-ia.onrender.com)

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11+ / FastAPI |
| Base de datos | PostgreSQL (prod) / SQLite (dev) |
| ORM | SQLAlchemy 2.0 async |
| Migraciones | Alembic |
| IA | LiteLLM (abstrae Anthropic, Ollama Cloud y Ollama Local) |
| Frontend | HTML5 + Tailwind CSS (CDN) + JS vanilla |
| Auth | JWT con python-jose (24 h, auto-logout en expiracion) |
| Deploy | Render.com / Docker |
| Tests | pytest + pytest-asyncio (backend) · Node.js stdlib (frontend) |

---

## Inicio Rapido (Local)

### Windows
```bash
cd dragons-ia
scripts\start_local.bat
```

### Linux / Mac
```bash
cd dragons-ia
chmod +x scripts/start_local.sh
./scripts/start_local.sh
```

### Manual
```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

pip install -r requirements.txt

cp .env.example .env
# Editar .env con tu API key

uvicorn backend.main:app --reload
```

Abri http://localhost:8000 en tu navegador.

---

## Configuracion de IA

El juego soporta multiples proveedores de IA a traves de LiteLLM:

| Proveedor | Modelo ejemplo | Configuracion |
|---|---|---|
| Anthropic | `claude-3-5-haiku-20241022` | API Key de Anthropic |
| Ollama Cloud | `ollama/gemma3:12b` | API Key de Ollama Cloud |
| Ollama Local | `ollama/llama3.2` | Ollama corriendo en tu PC (sin API key) |

### Anthropic (Claude)

1. Crea una cuenta en [console.anthropic.com](https://console.anthropic.com)
2. Genera una API Key
3. En el juego: **Configuracion → Anthropic → pega tu API Key**

### Ollama Cloud

1. Registrate en [ollama.com](https://ollama.com)
2. Obtene tu API Key desde **Settings → API Keys**
3. En el juego: **Configuracion → Ollama Cloud → elegi modelo → pega tu API Key**

**Modelos disponibles en Ollama Cloud (verificados):**

| Modelo | Tamaño | Ideal para |
|---|---|---|
| `gemma3:4b` | 4B | Pruebas rapidas |
| `gemma3:12b` | 12B | Buena narrativa |
| `gemma3:27b` | 27B | Narrativa avanzada |
| `ministral-3:8b` | 8B | Eficiente y preciso |
| `deepseek-v3.1:671b` | 671B | Maxima calidad |
| `qwen3.5:397b` | 397B | Maxima calidad |

### Ollama Local (gratis, sin API key)

1. Instala Ollama: [ollama.com/download](https://ollama.com/download)
2. Descarga un modelo: `ollama pull llama3.2`
3. En el juego: **Configuracion → Ollama Local → elegi el modelo**

> La API key se guarda **solo en tu navegador** (localStorage) — nunca se envia al servidor.

---

## Mundos disponibles

| Mundo | Descripcion | Fuente del juego |
|---|---|---|
| 🏰 Fantasia Medieval | Reinos, dragones, magia arcana | Cinzel |
| 🚀 Ciencia Ficcion | Naves, IAs rebeldes, megacorporaciones | Orbitron |
| 🌀 Isekai | Transportado a otro mundo | Philosopher |
| 💀 Fantasia Oscura | Horror, corrupcion, muerte | Crimson Text |

Cada mundo aplica automaticamente una fuente tipografica tematica durante la sesion de juego.

---

## Funcionalidades

- **Dungeon Master IA** — narracion por parrafos con encabezado distintivo
- **Personaje D&D 5e** — stats con Point Buy, HP calculado por clase
- **Dados interactivos** — d4 a d20, un tiro por turno; critico (Nat 20) y fallo total (Nat 1) con efectos visuales
- **Barra de HP / XP** — actualizacion en tiempo real con colores (verde → amarillo → rojo)
- **Partidas guardadas** — lista con icono de mundo, nombre del personaje y estado
- **Indicador de estado IA** — punto en el header: gris / amarillo pulsante / verde / rojo
- **Auto-logout** — detecta token expirado localmente y redirige al login con aviso
- **Retry automatico** — reintentos con backoff en errores 502/503/504 y de red
- **Acciones rapidas** — Atacar, Defenderse, Bolsa, Huir con un clic

---

## Estructura del Proyecto

```
dragons-ia/
├── backend/
│   ├── main.py              # Entry point FastAPI
│   ├── config.py            # Configuracion desde .env
│   ├── database.py          # SQLAlchemy async
│   ├── models/              # ORM: User, Character, SaveGame
│   ├── schemas/             # Pydantic: user, character, game
│   ├── routers/             # Endpoints: auth, characters, game
│   ├── services/            # ai_service, dungeon_master, dice
│   └── alembic/             # Migraciones DB
├── frontend/
│   ├── index.html           # Inicio / partidas guardadas
│   ├── login.html           # Login
│   ├── register.html        # Registro
│   ├── world.html           # Seleccion de mundo
│   ├── character.html       # Creacion de personaje
│   ├── confirm.html         # Confirmacion antes de jugar
│   ├── game.html            # Sesion de juego
│   ├── config.html          # Configuracion de IA
│   └── static/
│       ├── css/style.css    # Estilos globales + animaciones
│       └── js/
│           ├── api.js       # Fetch centralizado + retry + auto-logout
│           ├── auth.js      # JWT local + expiracion + logout
│           └── game.js      # Logica de juego, dados, fuentes, estado IA
├── tests/
│   ├── conftest.py          # Fixtures: BD en memoria, cliente HTTP, auth
│   ├── test_schemas.py      # Tests Pydantic (15)
│   ├── test_auth.py         # Tests endpoints auth (11)
│   ├── test_saves.py        # Tests partidas + JOIN character (10)
│   └── frontend/
│       └── test_game_logic.js  # Tests logica JS sin dependencias (26)
├── scripts/                 # Scripts de inicio y seed
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Dockerfile
└── render.yaml
```

---

## API Endpoints

### Auth
- `POST /auth/register` — Registro (retorna JWT)
- `POST /auth/login` — Login (retorna JWT)
- `GET /auth/me` — Perfil del usuario autenticado

### Personajes
- `POST /characters/` — Crear personaje
- `GET /characters/` — Listar personajes
- `GET /characters/{id}` — Obtener personaje
- `DELETE /characters/{id}` — Eliminar personaje

### Juego
- `POST /game/new` — Iniciar nueva partida (genera escena de apertura)
- `POST /game/action` — Enviar accion al DM
- `GET /game/saves` — Listar partidas (incluye nombre y mundo del personaje)
- `GET /game/saves/{id}` — Obtener partida con historial completo
- `POST /game/saves/{id}/save` — Guardar manualmente
- `DELETE /game/saves/{id}` — Eliminar partida

---

## Tests

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Backend (pytest)
pytest -v

# Frontend (Node.js, sin dependencias)
node tests/frontend/test_game_logic.js
```

**Estado actual: 62/62 tests pasando**

| Suite | Tests | Descripcion |
|---|---|---|
| `test_schemas.py` | 15 | Validacion Pydantic: stats, worlds, game actions |
| `test_auth.py` | 11 | Registro, login, duplicados, rutas protegidas |
| `test_saves.py` | 10 | JOIN character→save, aislamiento por usuario |
| `test_game_logic.js` | 26 | WORLD_FONTS, dados, XP/nivel, estados IA |

---

## Deploy en Render

1. Subi el repo a GitHub
2. Conecta el repo en [render.com](https://render.com)
3. El archivo `render.yaml` configura todo automaticamente
4. Agrega las variables de entorno en el dashboard de Render:

| Variable | Descripcion |
|---|---|
| `DATABASE_URL` | URL de PostgreSQL (Render la provee automaticamente) |
| `JWT_SECRET_KEY` | Clave secreta para firmar tokens (minimo 32 caracteres) |
| `DEBUG` | `false` en produccion |

> ⚠️ **Importante:** Configura `JWT_SECRET_KEY` como variable de entorno fija en Render.
> Si no esta configurada, cada restart genera tokens incompatibles con los anteriores,
> causando errores "Token invalido o expirado" al reiniciar el servidor.

---

## Licencia

Proyecto personal — Todos los derechos reservados.
