# ⚔️ Dragons & IA

> Juego de rol por texto impulsado por Inteligencia Artificial que actúa como Dungeon Master.

El jugador crea un personaje, elige un mundo y vive una aventura narrada en tiempo real por una IA.
Soporta múltiples modelos de IA: OpenAI (GPT), Anthropic (Claude) y modelos locales vía Ollama.

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11+ / FastAPI |
| Base de datos | PostgreSQL (prod) / SQLite (dev) |
| ORM | SQLAlchemy 2.0 async |
| Migraciones | Alembic |
| IA | LiteLLM (abstrae OpenAI, Anthropic, Ollama) |
| Frontend | HTML5 + Tailwind CSS (CDN) + JS vanilla |
| Auth | JWT con python-jose |
| Deploy | Render.com / Docker |

## Inicio Rápido (Local)

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
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu API key

# Iniciar servidor
uvicorn backend.main:app --reload
```

Abrí http://localhost:8000 en tu navegador.

## Configuración de IA

El juego soporta múltiples proveedores de IA a través de LiteLLM:

| Proveedor | Modelo ejemplo | Variable de entorno |
|-----------|---------------|-------------------|
| OpenAI | `gpt-4o-mini` | `OPENAI_API_KEY` |
| Anthropic | `claude-3-haiku-20240307` | `ANTHROPIC_API_KEY` |
| Ollama | `ollama/llama3` | `OLLAMA_API_BASE` |

Configurá tu API key en `.env` o directamente desde la pantalla de Configuración del juego.

## Estructura del Proyecto

```
dragons-ia/
├── backend/
│   ├── main.py              # Entry point FastAPI
│   ├── config.py            # Configuración desde .env
│   ├── database.py          # SQLAlchemy async
│   ├── models/              # Modelos ORM (User, Character, SaveGame)
│   ├── schemas/             # Schemas Pydantic
│   ├── routers/             # Endpoints API (auth, characters, game, donations)
│   ├── services/            # AI service, Dungeon Master, dados
│   └── alembic/             # Migraciones DB
├── frontend/
│   ├── *.html               # Páginas del juego
│   └── static/              # CSS + JS
├── scripts/                 # Scripts de inicio y datos seed
├── requirements.txt
├── Dockerfile
└── render.yaml              # Config de deploy en Render
```

## API Endpoints

### Auth
- `POST /auth/register` — Registro de usuario
- `POST /auth/login` — Login (retorna JWT)
- `GET /auth/me` — Perfil del usuario autenticado

### Personajes
- `POST /characters/` — Crear personaje
- `GET /characters/` — Listar personajes
- `GET /characters/{id}` — Obtener personaje
- `DELETE /characters/{id}` — Eliminar personaje

### Juego
- `POST /game/new` — Iniciar nueva partida
- `POST /game/action` — Enviar acción al DM
- `GET /game/saves` — Listar partidas guardadas
- `GET /game/saves/{id}` — Obtener partida con historial

### Donaciones
- `GET /donations/info` — Links de donación

## Deploy en Render

1. Subí el repo a GitHub
2. Conectá el repo en [render.com](https://render.com)
3. El archivo `render.yaml` configura todo automáticamente
4. Agregá las variables de entorno (API keys) en el dashboard de Render

## Licencia

Proyecto personal — Todos los derechos reservados.
