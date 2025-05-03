FROM python:3.13.2-slim-bookworm

# Обновляем систему и ставим системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем pip и wheel (для сборки Python-зависимостей)
RUN pip install --upgrade pip wheel

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем порт FastAPI
EXPOSE 8000

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
# Запуск сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]