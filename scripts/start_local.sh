#!/bin/bash
# ══════════════════════════════════════════════
# Dragons & IA — Script de inicio local (Linux/Mac)
# ══════════════════════════════════════════════
set -e

echo "⚔️  Dragons & IA — Inicio local"
echo "════════════════════════════════════"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instalalo antes de continuar."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt --quiet

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde template..."
    cp .env.example .env
    echo "⚠️  Editá .env con tus API keys antes de jugar."
fi

# Iniciar servidor
echo ""
echo "🚀 Iniciando servidor en http://localhost:8000"
echo "   Presioná Ctrl+C para detener."
echo "════════════════════════════════════"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
