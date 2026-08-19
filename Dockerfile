# Builder stage
FROM python:3.11.6-slim-bookworm AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install --no-install-recommends -y build-essential \
    && pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY src/ ./src/

# Runtime stage (minimal)
FROM python:3.11.6-slim-bookworm AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy installed packages only
COPY --from=builder /install /usr/local

# Copy source code
COPY --from=builder /app/src ./src

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "src/app.py"]