FROM python:3.12-slim

WORKDIR /app

# Install piper-tts
RUN pip install --no-cache-dir "piper-tts>=1.2.0,<2.0.0"

# Create non-root user
RUN groupadd -r piper && useradd -r -g piper -d /app piper

COPY --chown=piper:piper main.py .

EXPOSE 5000

USER piper

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health', timeout=5)" || exit 1

CMD ["python", "main.py"]
