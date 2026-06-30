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

## Deployment & Infrastructure

### Render.com
- Primary deployment platform
- Uses render.yaml for automatic configuration
- Environment variables: DATABASE_URL, JWT_SECRET_KEY, DEBUG

### Docker
- Dockerfile for containerization
- docker-compose.yml for local development
- Image: dragons-ia

## Authentication & Security

### JWT Authentication
- python-jose library
- 24-hour token expiration
- Auto-logout on token expiration
- Local storage of tokens (never sent to server)

## Testing

### Backend
- pytest with pytest-asyncio
- 62/62 tests passing
- Tests for schemas, auth, saves, game logic

### Frontend
- Node.js stdlib for testing game logic
- 26 tests passing

## Monitoring & Diagnostics

### Ollama Status Detection
- Endpoint: GET /api/system/ollama-status
- Real-time frontend diagnostics in config.html
- Automatic fallback when models not installed
- RAM-based model recommendations