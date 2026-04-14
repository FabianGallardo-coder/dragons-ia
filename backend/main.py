"""
Dragons & IA — Entry point de la aplicación FastAPI.

Monta los routers de la API, sirve el frontend estático
y gestiona el ciclo de vida de la base de datos.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import get_settings
from backend.database import create_tables
from backend.routers import auth, characters, game, donations

settings = get_settings()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas de la BD al iniciar si no existen."""
    await create_tables()
    yield


app = FastAPI(
    title="Dragons & IA",
    description="Juego de rol por texto impulsado por Inteligencia Artificial.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers de la API ──────────────────────────────────────────
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(characters.router, prefix="/characters", tags=["Characters"])
app.include_router(game.router, prefix="/game", tags=["Game"])
app.include_router(donations.router, prefix="/donations", tags=["Donations"])

# ── Archivos estáticos del frontend ────────────────────────────
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


# ── Servir páginas HTML del frontend ───────────────────────────
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/{page}.html", include_in_schema=False)
async def serve_page(page: str):
    """Sirve cualquier página HTML del frontend."""
    file_path = FRONTEND_DIR / f"{page}.html"
    if file_path.is_file():
        return FileResponse(str(file_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))
