# =============================================================================
# Build stage
# =============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# =============================================================================
# Runtime stage
# =============================================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# Crear usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar solo dependencias de runtime necesarias (sin MySQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas del builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código fuente
COPY --chown=appuser:appuser . .

# Dar permisos de escritura a appuser sobre /app (necesario para SQLite)
RUN chown appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Asegurar que pip user packages están en PATH
ENV PATH="/home/appuser/.local/bin:${PATH}" \
    PYTHONUNBUFFERED=1

# Puerto
EXPOSE 8000

# Health check (usa urllib de stdlib, sin dependencias extra)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)" || exit 1

# Comando de inicio
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
