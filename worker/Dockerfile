# ---- Build Stage ----
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Final Stage ----
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy app code
COPY . .

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

HEALTHCHECK CMD python -c "import os; exit(0 if os.path.exists('worker.py') else 1)"

# Run app
CMD ["python", "worker.py"]