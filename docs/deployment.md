# Deployment Guide

## Local Development

### Windows
```bash
scripts\start_local.bat
```

### Linux / Mac
```bash
chmod +x scripts/start_local.sh
./scripts/start_local.sh
```

### Manual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt

cp .env.example .env
# Editar .env con tu API key

uvicorn backend.main:app --reload
```

Open http://localhost:8000

### Environment Variables (.env)
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database URL | `sqlite+aiosqlite:///./dragons_ia.db` |
| `JWT_SECRET_KEY` | JWT signing secret (min 32 chars) | Auto-generated in dev |
| `DEBUG` | Debug mode | `true` |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional) | `` |
| `OLLAMA_API_BASE` | Ollama server URL | `http://localhost:11434` |

## Production (Render.com)
1. Push to GitHub
2. Connect repo on [render.com](https://render.com)
3. `render.yaml` auto-configures everything
4. Set environment variables in Render dashboard:
   - `DATABASE_URL` — PostgreSQL (Render provides automatically)
   - `JWT_SECRET_KEY` — Random 32+ char secret (set once; changing invalidates tokens)
   - `DEBUG` — `false`

## Docker
```bash
# Build
docker build -t dragons-ia .

# Run
docker run -p 8000:8000 dragons-ia

# Or with docker-compose
docker-compose up
```

### Docker + Ollama Local (host access)
Inside Docker, `localhost` refers to the container, not the host. To connect to Ollama running on the host:

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - OLLAMA_API_BASE=http://host.docker.internal:11434
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

- `host.docker.internal` resolves to the host machine on Windows/Mac
- On Linux, `host-gateway` maps to the Docker host

## Piper TTS (Optional)
For higher quality voice narration, install Piper TTS on the server:
```bash
pip install piper-tts
# The voice model is bundled at backend/piper_voices/es_MX/claude/high/
```

**Note**: Piper requires `espeak-ng` at runtime for phonemization. On Debian/Ubuntu:
```bash
apt-get install espeak-ng
```

## Content Security Policy
The app sets CSP headers including `media-src 'self' blob:` to allow TTS audio playback via blob URLs. If you add custom media handling, ensure the CSP doesn't block it.

## Important Notes
- ⚠️ `JWT_SECRET_KEY` must be a fixed value in production. Changing it invalidates all existing tokens.
- API keys are stored in the browser (localStorage), never on the server.
- Ollama Local requires the user to have Ollama running on their machine.
- `@asynccontextmanager` on FastAPI dependencies causes `TypeError` — use plain `async def` with `yield` instead.
