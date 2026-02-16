# Используем официальный минимальный Python образ
FROM python:3.14-slim

# Обновляем PIP
RUN pip install --upgrade pip

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Создаем не-root пользователя для безопасности
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

# Запускаем приложение
CMD ["python", "main.py"]
