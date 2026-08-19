# -------- Builder Stage --------
FROM python:3.11.8-slim-bookworm AS builder

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Update system packages (patch CVEs) and install build tools
RUN apt-get update && apt-get upgrade -y && \
    apt-get install --no-install-recommends -y build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install into /install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Copy source code
COPY src/ ./src/

# -------- Runtime Stage --------
FROM python:3.11.8-slim-bookworm AS runtime

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Update runtime system packages (patch CVEs)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Copy only installed packages from builder
COPY --from=builder /install /usr/local

# Copy source code from builder
COPY --from=builder /app/src ./src

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose Flask default port
EXPOSE 5000

# Healthcheck for orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the Flask app
CMD ["python", "src/app.py"]