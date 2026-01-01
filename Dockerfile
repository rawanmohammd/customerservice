# Backend Dockerfile for Hugging Face Spaces
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Expose port (Hugging Face Spaces defaults to 7860)
EXPOSE 7860

# Force Cache Bust via Env Var
ENV CACHE_BUST="2026-01-01T22:45"

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
