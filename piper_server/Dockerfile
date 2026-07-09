FROM python:3.12-slim

WORKDIR /app

# Instalar piper-tts
RUN pip install --no-cache-dir piper-tts>=1.2.0,<2.0.0

# Copiar el servidor HTTP
COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
