# Build stage
FROM python:3.14-slim AS builder
RUN pip install --no-cache-dir --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --target=/install \
    -r requirements.txt

# Production stage
FROM python:3.14-slim
LABEL maintainer="Codeyro Production"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN useradd -m -u 1000 appuser
WORKDIR /app

# Copy app packages and dependencies from builder stage
COPY --from=builder /install /usr/local/lib/python3.14/site-packages
COPY --from=builder /install/bin/* /usr/local/bin/
COPY --chown=appuser:appuser main.py .

USER appuser

CMD ["python", "main.py"]
