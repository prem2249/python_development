# -------- Builder Stage --------
FROM python:3.11.8-alpine3.20 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Update Alpine packages and install build dependencies
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache build-base

# Copy requirements and install into /install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/

# -------- Runtime Stage --------
FROM python:3.11.8-alpine3.20 AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Apply Alpine security updates
RUN apk update && apk upgrade --no-cache

# Copy installed packages and app code
COPY --from=builder /install /usr/local
COPY --from=builder /app/src ./src
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/static ./static

# Create non-root user
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Healthcheck for orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "src/app.py"]