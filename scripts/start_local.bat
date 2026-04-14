@echo off
REM ══════════════════════════════════════════════
REM Dragons & IA — Script de inicio local (Windows)
REM ══════════════════════════════════════════════

echo ⚔️  Dragons ^& IA — Inicio local
echo ════════════════════════════════════

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Instalalo antes de continuar.
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt --quiet

REM Crear .env si no existe
if not exist ".env" (
    echo 📝 Creando archivo .env desde template...
    copy .env.example .env
    echo ⚠️  Edita .env con tus API keys antes de jugar.
)

REM Iniciar servidor
echo.
echo 🚀 Iniciando servidor en http://localhost:8000
echo    Presiona Ctrl+C para detener.
echo ════════════════════════════════════
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
