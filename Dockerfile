# Dockerfile

# Используем базовый образ Python
FROM python:3.11-slim

# Установка переменной окружения для Python
ENV PYTHONUNBUFFERED=1

# Установка poetry
RUN pip install poetry

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование зависимостей проекта и установка их через poetry
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Копирование проекта в контейнер
COPY . /app/

# Запуск сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

