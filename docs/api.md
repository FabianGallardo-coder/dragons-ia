# API Reference

## Authentication
All protected endpoints require `Authorization: Bearer <token>` header.

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Register new user (returns JWT) |
| POST | `/auth/login` | No | Login (returns JWT) |
| POST | `/auth/forgot-password` | No | Request password reset (returns token in debug) |
| POST | `/auth/reset-password` | No | Reset password with token |
| GET | `/auth/me` | Yes | Current user profile |

## Characters

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/characters/` | Yes | Create character (name, race, class, stats, world) |
| GET | `/characters/` | Yes | List user's characters |
| GET | `/characters/{id}` | Yes | Get character details |
| PUT | `/characters/{id}` | Yes | Update character (name, race, class, stats, etc.) |
| DELETE | `/characters/{id}` | Yes | Delete character |

### Character Schema
```json
{
  "name": "Aragorn",
  "race": "Humano",
  "character_class": "Guerrero",
  "world": "fantasia",
  "stats": {"strength": 15, "dexterity": 14, "constitution": 13, "intelligence": 10, "wisdom": 12, "charisma": 8},
  "hp_current": 12,
  "hp_max": 12,
  "level": 1
}
```

## Game

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/game/new` | Yes | Start new game (generates opening scene via AI) |
| POST | `/game/action` | Yes | Send player action to DM |
| GET | `/game/saves` | Yes | List saves (with character name + world) |
| GET | `/game/saves/{id}` | Yes | Get save with full history |
| POST | `/game/saves/{id}/save` | Yes | Manual save |
| DELETE | `/game/saves/{id}` | Yes | Delete save |
| GET | `/game/ollama/models` | No | List locally installed Ollama models |
| POST | `/game/ollama/models/cloud` | No | List Ollama Cloud models (requires api_key) |

### POST /game/action
```json
{
  "save_id": "uuid",
  "action": "Ataco al goblin con mi espada",
  "dice_result": 15,
  "ai_model": "claude-sonnet-4-20250514",
  "api_key": "sk-ant-..."
}
```

### Response
```json
{
  "narrative": "El goblin esquiva tu ataque...",
  "character_hp": 10,
  "character_hp_max": 12,
  "character_xp": 45,
  "character_alive": true,
  "turn_count": 3
}
```

## System

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/system/ollama-status` | No | Ollama diagnostics (running, models, RAM, recommendations) |
| GET | `/health` | No | Health check |
| GET | `/ready` | No | Readiness check |

## TTS

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/tts/status` | No | Piper TTS availability check |
| POST | `/api/tts` | No | Generate speech from text (returns WAV audio) |

### POST /api/tts
```json
{
  "text": "El dragón emerge de las sombras...",
  "voice": "es_MX/claude/high/es_MX-claude-high"
}
```
