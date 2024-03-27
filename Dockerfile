# Dockerfile

# Используем базовый образ Python 3.11
FROM python:3.11-slim

# Установка переменной окружения для Python
ENV PYTHONUNBUFFERED=1

# Установка poetry
RUN pip install poetry

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование зависимостей проекта и установка их через poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Копирование проекта в контейнер
COPY . /app/

# Запуск сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
