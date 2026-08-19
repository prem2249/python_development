# Use a pinned slim Python image
FROM python:3.11.6-slim AS base

# Environment settings for security and performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install security updates and essential build tools
RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies securely (versions pinned in requirements.txt)
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy only source code
COPY src/ ./src/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Flask default port (HTTP)
EXPOSE 5000

# Add a healthcheck for container orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the Flask app
CMD ["python", "src/app.py"]