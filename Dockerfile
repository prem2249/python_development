#FROM python:3.11.8-alpine3.19 AS builder
FROM python:3.11-alpine3.24 AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Update Alpine packages to patched versions
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache \
      util-linux \
      openssl \
      sqlite \
      build-base

# Copy requirements and install into /install
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

COPY src/ ./src/

# -------- Runtime Stage --------
FROM python:3.11-alpine3.24 AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache \
      util-linux \
      openssl \
      sqlite

COPY --from=builder /install /usr/local
COPY --from=builder /app/src ./src

RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "src/app.py"]