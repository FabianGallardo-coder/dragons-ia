# Architecture

The Dragons-IA project employs a client-server architecture, with a Python-based backend handling game logic and AI functionalities, and a JavaScript-driven frontend for user interaction.

## Backend

The backend is primarily developed in Python and appears to leverage a web framework (likely FastAPI, inferred from file structure and common Python web development patterns). It manages core game mechanics, AI integrations (like TTS and potentially other AI services), user authentication, and data persistence.

Key components observed in the backend include:

*   **`backend/main.py`**: The entry point for the backend application.
*   **`backend/routers/`**: Contains modules for defining API endpoints, such as `game.py`, `auth.py`, and `tts.py`. This suggests a RESTful API design.
*   **`backend/services/`**: Houses the business logic and core functionalities, including `dungeon_master.py` for game narrative and AI, and `tts_service.py` for text-to-speech.
*   **`backend/schemas/`**: Likely defines data structures and validation models (e.g., using Pydantic, common with FastAPI).
*   **Database Integration**: The presence of `backend/database.py`, `backend/models/` and `alembic.ini` indicates the use of an ORM (Object-Relational Mapper) like SQLAlchemy and a database migration tool.

## Frontend

The frontend is responsible for rendering the game interface and handling user input. It is built using standard web technologies:

*   **HTML**: Defines the structure of the web pages (e.g., `frontend/game.html`, `frontend/index.html`).
*   **CSS**: Styles the user interface for a visually appealing experience (e.g., `frontend/static/css/style.css`).
*   **JavaScript**: Implements client-side logic, interactivity, API calls to the backend, and dynamic content rendering (e.g., `frontend/static/js/game.js`, `frontend/static/js/api.js`). Recent commits also show a significant addition of immersion-related JavaScript files (`frontend/static/js/immersion/`).

## Text-to-Speech (TTS) Integration

A dedicated `piper_server/` directory and related services (`backend/services/tts_service.py`, `frontend/static/js/tts.js`) suggest a robust TTS integration. This component likely handles the conversion of game text into spoken audio for an enhanced immersive experience.

## AI Services

Beyond TTS, the presence of services like `dungeon_master.py` and potentially AI-related modules (`backend/services/ai_service.py` might be related, though it was modified/removed in some commits) indicates that AI plays a central role in generating dynamic content, NPC interactions, and overall game narrative. Ollama integration for system detection and model fallback is also evident.

## Deployment and Infrastructure

*   **Docker**: Dockerfiles (`Dockerfile`, `piper_server/Dockerfile`) and `docker-compose.yml` are present, indicating containerization for development and deployment.
*   **Configuration**: `.env.example` files suggest environment-based configuration for sensitive settings and service parameters.
*   **Cloud Deployment**: `render.yaml` implies potential deployment on cloud platforms like Render.

## Source Map

*   `/backend`: Python codebase for the server-side logic.
*   `/frontend`: HTML, CSS, and JavaScript for the client-side interface.
*   `/tests`: Test suites.
*   `/piper_server`: Dedicated TTS server.
*   `/scripts`: Helper scripts.
*   `/docs`: Ancillary documentation files.
*   `/openwiki`: Generated documentation.

This architecture allows for a scalable and maintainable application, with clear separation of concerns between the frontend and backend. The integration of AI and TTS features aims to provide a rich, interactive, and immersive gaming experience.