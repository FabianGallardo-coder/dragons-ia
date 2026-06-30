# System Architecture

## Overview
Dragons & IA is a text-based RPG powered by AI that acts as a Dungeon Master, allowing players to create characters, choose worlds, and experience adventures narrated in real-time by artificial intelligence.

## Components
- Backend: FastAPI, Python 3.11+
- Database: PostgreSQL/SQLite with SQLAlchemy
- Frontend: HTML5, Tailwind CSS, Vanilla JS
- AI Services: Anthropic, Ollama Cloud, Ollama Local via LiteLLM

## Data Flow
1. User interacts with frontend
2. Frontend sends requests to backend API
3. Backend processes with AI services
4. Database stores game state
5. Response returned to frontend