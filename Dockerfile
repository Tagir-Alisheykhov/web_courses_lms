# Build stage
FROM python:3.11 as builder
WORKDIR /app

# Install Poetry and dependencies
RUN pip install --no-cache-dir "poetry==2.1.1" && \
    poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Copy installed dependencies
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Install runtime deps and Gunicorn
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir gunicorn==21.2.0

# Copy application code
COPY . .

# Gunicorn config
ENV GUNICORN_CMD_ARGS="--workers=4 --threads=2 --timeout=60 --bind=0.0.0.0:8000"

# Run command
CMD ["gunicorn", "config.wsgi:application"]
