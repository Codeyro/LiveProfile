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

ARG TZ
ARG API_ID
ARG API_HASH
ARG SESSION_STRING

ENV TZ=$TZ \
    API_ID=$API_ID \
    API_HASH=$API_HASH \
    SESSION_STRING=$SESSION_STRING\
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN useradd -m -u 1000 appuser
WORKDIR /app

# Копируем только установленные пакеты из стадии builder
COPY --from=builder /install /usr/local/lib/python3.14/site-packages
COPY --from=builder /install/bin/* /usr/local/bin/

# Копируем только главный файл приложения
COPY --chown=appuser:appuser main.py .

# Переключаемся на не-root пользователя
USER appuser

# Запускаем приложение
CMD ["python", "main.py"]
