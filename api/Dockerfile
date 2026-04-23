# ---- Build Stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

COPY api/ /app/api/

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Final Stage ----
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy app code
COPY api/ /app/api/

RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:8000/health || exit 1

# Run app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]