# Deployment Guide

## Local Development
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Set up .env file
5. Run uvicorn backend.main:app --reload

## Production (Render.com)
1. Push to GitHub
2. Connect repo to Render.com
3. Set environment variables
4. Deploy

## Docker
1. Build: docker build -t dragons-ia .
2. Run: docker run -p 8000:8000 dragons-ia