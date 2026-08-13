FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN adduser -D -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser utils.py .
COPY --chown=appuser:appuser fonts/ ./fonts/

USER appuser

CMD ["python", "main.py"]