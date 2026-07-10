# Data Models and Storage

The project utilizes a relational database for persistent storage, managed by SQLAlchemy as the Object-Relational Mapper (ORM) and Alembic for database migrations.

## Database Schema

The core data entities managed by the application are:

*   **`User`**:
    *   Stores user account credentials and basic information.
    *   Fields include `id` (UUID), `email`, `username`, `password_hash`, `is_active`, `created_at`, and `updated_at`.
    *   Has a one-to-many relationship with `Character` and `SaveGame`.
    *   *Source*: `/backend/models/user.py`

*   **`Character`**:
    *   Represents an individual player character.
    *   Fields include `id` (UUID), `user_id`, `name`, `world`, `race`, `gender`, `character_class`, `unique_object`, game `stats` (stored as a JSON string), `hp_max`, `hp_current`, `level`, `experience`, and `is_alive`.
    *   Has a one-to-many relationship with `SaveGame`.
    *   *Source*: `/backend/models/character.py`

*   **`SaveGame`**:
    *   Stores the state of a saved game session.
    *   Fields include `id` (UUID), `user_id`, `character_id`, `title`, `history` (conversation log stored as a JSON string), `turn_count`, `is_active`, `created_at`, and `updated_at`.
    *   *Source*: `/backend/models/save.py`

*   **`ResetToken`**:
    *   Manages tokens used for password reset workflows.
    *   Fields include `id` (UUID), `user_id`, `token`, `expires_at`, `used` status, and `created_at`.
    *   *Source*: `/backend/models/reset_token.py`

## Database Management

*   **ORM**: SQLAlchemy is used for defining models and interacting with the database. The `Base` class from `backend.database` serves as the declarative base for all models.
*   **Migrations**: Alembic is employed to manage database schema evolution. Migration scripts are located in `/backend/alembic/versions/`.
*   **Database Files**: During development, SQLite databases (`dragons_ia.db`, `test_dragons_tmp.db`) may be used, as suggested by their presence in the root directory. Production environments likely use a more robust database system.

## Data Storage Patterns

*   **UUIDs**: Primary keys for most entities are generated as UUIDs, ensuring unique identifiers across distributed systems.
*   **JSON for Complex Data**: Attributes like `stats` and `history` are stored as JSON strings within `TEXT` columns. This allows for flexible storage of dynamic or structured data within a relational model.
*   **Timestamps**: Standard `created_at` and `updated_at` fields are maintained for most models, facilitating auditing and tracking of data changes.
*   **Foreign Keys**: Relationships between tables are enforced using foreign keys, with `ondelete="CASCADE"` specified for some relationships, meaning related data is removed when the parent record is deleted (e.g., deleting a user deletes their characters and save games).
