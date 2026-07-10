# Testing and Integrations

## Testing Strategy

The project employs a robust testing strategy to ensure the quality and reliability of its backend services and game logic.

*   **Unit and Integration Testing**: The primary testing framework used is `pytest`, as indicated by `requirements-dev.txt`. The test suite includes:
    *   **Backend Tests**: Found within the `/tests` directory, these tests cover various aspects of the backend functionality, including authentication (`test_auth.py`), game logic (`test_game.py`), and character management.
    *   **Frontend Tests**: Although not deeply explored in this run, the presence of files like `tests/frontend/test_game_logic.js` suggests frontend-specific tests may also exist.
    *   **Dependencies**: Development dependencies like `pytest` and `pytest-asyncio` are listed in `requirements-dev.txt`.

*   **Mocking**: Key external service interactions, particularly AI responses, are mocked using `unittest.mock.patch` (likely from Python's standard library). This allows for isolated testing of the application's logic without relying on live AI services. For example, `backend/routers/game.py` uses `patch` to mock `get_ai_response`.

*   **API Testing**: `AsyncClient` from `httpx` is used within the tests to make asynchronous HTTP requests to the backend API, simulating client interactions.

*   **Test Database**: Separate SQLite databases (`dragons_ia.db`, `test_dragons_tmp.db`) suggest that tests might run against an isolated database instance to avoid conflicts with the development or production database.

## Integrations

The project integrates with several external services and systems:

*   **PostgreSQL**: The primary persistent data store, managed via SQLAlchemy and Alembic.
*   **Ollama**: Integrated for AI-powered gameplay, likely for Natural Language Understanding (NLU), text generation, and potentially other AI-driven features. The `OLLAMA_API_BASE` environment variable in `docker-compose.yml` points to the Ollama service.
*   **Piper TTS**: Used for Text-to-Speech functionality, enabling voice output for in-game narration and dialogue. The `TTS_URL` and `TTS_VOICE` environment variables configure this integration.
*   **Docker & Docker Compose**: Used for containerization and orchestration, ensuring a consistent and reproducible deployment environment.

## Git Usage

*   **Commit History**: The project has a clear commit history (`git log`) showing significant development activity, including feature implementations (TTS, Ollama, AI detection), bug fixes, documentation updates, and test suite additions.
*   **Branching**: The presence of branches like `worktree-documentation-update` and merge commits suggests a standard Git workflow.
*   **`requirements-dev.txt`**: This file specifically lists development and testing dependencies, separating them from the main application requirements.

## Documentation

*   **Existing Docs**: The `/docs` directory contains various architectural and deployment-related documents.
*   **OpenWiki**: New documentation will be systematically generated under the `/openwiki` directory, starting with `quickstart.md`.
