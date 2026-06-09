# Project Inventory

## Directory Structure

```
dragons-ia/
├── .env.example
├── .gitignore
├── .pytest_cache/
│   ├── README.md
│   └── ... (cache files)
├── alembic.ini
├── backend/
│   ├── __pycache__/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── .gitkeep
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── character.py
│   │   ├── save.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── auth.py
│   │   ├── characters.py
│   │   ├── game.py
│   │   └── donations.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── character.py
│   │   ├── game.py
│   │   └── user.py
│   └── services/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── ai_service.py
│       ├── dice.py
│       └── dungeon_master.py
├── Dockerfile
├── frontend/
│   ├── character.html
│   ├── config.html
│   ├── confirm.html
│   ├── game.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── world.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── api.js
│           ├── auth.js
│           ├── character.js
│           └── game.js
├── pytest.ini
├── README.md
├── render.yaml
├── requirements-dev.txt
├── requirements.txt
├── scripts/
│   ├── seed_data.py
│   ├── start_local.bat
│   └── start_local.sh
├── test_dragons_tmp.db
└── tests/
    ├── __init__.py
    ├── __pycache__/
    ├── conftest.py
    ├── test_auth.py
    ├── test_saves.py
    ├── test_schemas.py
    └── frontend/
        └── test_game_logic.js
```

## File List

- .env.example
- .gitignore
- .pytest_cache/README.md
- alembic.ini
- backend/__pycache__/config.cpython-313.pyc
- backend/__pycache__/database.cpython-313.pyc
- backend/__pycache__/main.cpython-313.pyc
- backend/alembic/env.py
- backend/alembic/script.py.mako
- backend/alembic/versions/.gitkeep
- backend/config.py
- backend/database.py
- backend/main.py
- backend/models/__init__.py
- backend/models/__pycache__/__init__.cpython-313.pyc
- backend/models/__pycache__/character.cpython-313.pyc
- backend/models/__pycache__/save.cpython-313.pyc
- backend/models/__pycache__/user.cpython-313.pyc
- backend/models/character.py
- backend/models/save.py
- backend/models/user.py
- backend/routers/__init__.py
- backend/routers/__pycache__/__init__.cpython-313.pyc
- backend/routers/__pycache__/auth.cpython-313.pyc
- backend/routers/__pycache__/characters.cpython-313.pyc
- backend/routers/__pycache__/game.cpython-313.pyc
- backend/routers/__pycache__/donations.cpython-313.pyc
- backend/routers/auth.py
- backend/routers/characters.py
- backend/routers/game.py
- backend/routers/donations.py
- backend/schemas/__init__.py
- backend/schemas/__pycache__/__init__.cpython-313.pyc
- backend/schemas/__pycache__/character.cpython-313.pyc
- backend/schemas/__pycache__/game.cpython-313.pyc
- backend/schemas/__pycache__/user.cpython-313.pyc
- backend/schemas/character.py
- backend/schemas/game.py
- backend/schemas/user.py
- backend/services/__init__.py
- backend/services/__pycache__/__init__.cpython-313.pyc
- backend/services/__pycache__/ai_service.cpython-313.pyc
- backend/services/__pycache__/dice.cpython-313.pyc
- backend/services/__pycache__/dungeon_master.cpython-313.pyc
- backend/services/ai_service.py
- backend/services/dice.py
- backend/services/dungeon_master.py
- Dockerfile
- frontend/character.html
- frontend/config.html
- frontend/confirm.html
- frontend/game.html
- frontend/index.html
- frontend/login.html
- frontend/register.html
- frontend/world.html
- frontend/static/css/style.css
- frontend/static/js/api.js
- frontend/static/js/auth.js
- frontend/static/js/character.js
- frontend/static/js/game.js
- pytest.ini
- README.md
- render.yaml
- requirements-dev.txt
- requirements.txt
- scripts/seed_data.py
- scripts/start_local.bat
- scripts/start_local.sh
- test_dragons_tmp.db
- tests/__init__.py
- tests/__pycache__/__init__.cpython-313.pyc
- tests/__pycache__/conftest.cpython-313-pytest-8.4.1.pyc
- tests/__pycache__/test_auth.cpython-313-pytest-8.4.1.pyc
- tests/__pycache__/test_saves.cpython-313-pytest-8.4.1.pyc
- tests/__pycache__/test_schemas.cpython-313-pytest-8.4.1.pyc
- tests/conftest.py
- tests/test_auth.py
- tests/test_saves.py
- tests/test_schemas.py
- tests/frontend/test_game_logic.js