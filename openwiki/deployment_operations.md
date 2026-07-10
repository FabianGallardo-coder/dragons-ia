# Deployment and Operations

This project employs a containerized deployment strategy using Docker and Docker Compose, enabling consistent environments across development and production.

## Containerization

*   **Backend Application**: The main application is containerized using a Python 3.12 slim image. The `Dockerfile` in the repository root outlines the build process:
    *   It installs necessary system dependencies (like `gcc`, `libpq-dev` for build, and `libpq5` for runtime).
    *   Python dependencies are managed via `requirements.txt`.
    *   A non-root user (`appuser`) is created for enhanced security.
    *   The application is served using Uvicorn on port 8000.
    *   A `HEALTHCHECK` instruction is included in the `Dockerfile` for health monitoring.

*   **Database (PostgreSQL)**: A PostgreSQL database is run as a separate service using the `postgres:16-alpine` image.
    *   It's configured with specific environment variables for user, password, and database name.
    *   A persistent volume (`postgres_data`) is used to store database files.
    *   A `healthcheck` is defined to ensure the database is ready before the application attempts to connect.

*   **Text-to-Speech (TTS) Service**: A dedicated service (`piper-tts`) runs the TTS functionality.
    *   It's built from the `./piper_server` directory.
    *   Voice files are mounted from `./backend/piper_voices` into the container.

## Orchestration with Docker Compose

The `docker-compose.yml` file defines and orchestrates all the services:

*   **`postgres`**: The PostgreSQL database service.
*   **`piper-tts`**: The TTS service.
*   **`app`**: The main backend application service.

Key configurations within `docker-compose.yml`:

*   **Networking**: Services communicate over a Docker network. The application can reach the database via `postgres:5432` and the TTS service via `piper-tts:5000`.
*   **Environment Variables**: Crucial settings such as `DATABASE_URL`, `JWT_SECRET_KEY`, `OLLAMA_API_BASE`, `TTS_ENABLED`, and `TTS_URL` are injected via environment variables.
*   **Dependencies**: The `app` service explicitly depends on the `postgres` service, ensuring it starts only after the database is healthy.
*   **Volume Mounts**:
    *   `./frontend:/app/frontend:ro`: Mounts the frontend code for serving.
    *   `./backend/piper_voices:/app/backend/piper_voices:ro`: Mounts TTS voice files.
*   **Ollama Integration**: The `app` service is configured to connect to Ollama using `host.docker.internal:11434`, allowing it to access Ollama running on the host machine.
*   **Port Mapping**: The application's port 8000 is mapped to the host's port 8000.

## Development Setup

To run the project locally, you would typically:

1.  Ensure Docker and Docker Compose are installed.
2.  Clone the repository.
3.  Run `docker-compose up` in the project's root directory.

This command will build the images (if not already built) and start all defined services according to the `docker-compose.yml` configuration.

## Production Considerations

*   **`JWT_SECRET_KEY`**: The development key (`dev-secret-key-change-in-production`) must be replaced with a strong, securely generated secret in a production environment.
*   **Database Persistence**: The use of `volumes` for PostgreSQL ensures data persistence. In production, consider using managed database services or more robust storage solutions.
*   **Logging**: The `backend/logging_config.py` file (though not detailed in Docker config) likely handles logging configuration, which should be managed for production monitoring.
*   **Environment Variables**: Production configuration should be managed securely, potentially using Docker secrets or other configuration management tools.
*   **Ollama Host**: The `host.docker.internal` configuration is specific to Docker Desktop and may require adjustment in other Docker environments (e.g., using network configurations or a dedicated Ollama container).
