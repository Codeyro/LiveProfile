# Используем официальный Python образ с минимальным размером
FROM python:3.14-slim

# Обновляем PIP
RUN pip install --upgrade pip

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Создаем не-root пользователя для безопасности
RUN useradd -m -u 1000 teleuser && chown -R teleuser:teleuser /app
USER teleuser

# Запускаем приложение
CMD ["python", "main.py"]
