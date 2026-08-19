# -------- Builder Stage --------
FROM python:3.11.8-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache build-base

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

COPY src/ ./src/

# -------- Runtime Stage --------
FROM python:3.11.8-alpine AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy installed packages and app code
COPY --from=builder /install /usr/local
COPY --from=builder /app/src ./src

# Create non-root user
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "src/app.py"]