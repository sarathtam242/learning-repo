# Stage 1: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /build

# Create an isolated virtual environment
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime image
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Create a non-root user and log directory
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --uid 10001 appuser \
    && mkdir -p /app/logs \
    && chown -R appuser:appgroup /app

# Copy application source
COPY --chown=appuser:appgroup app/ ./app/

# Persistent log directory
VOLUME ["/app/logs"]

# Application port
EXPOSE 8080

# Run as non-root user
USER appuser

# Container health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)" || exit 1

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
