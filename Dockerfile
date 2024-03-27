# Dockerfile

# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменную среды для рабочей директории
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Устанавливаем зависимости
ENV PYTHONPATH "${APP_HOME}:${APP_HOME}/drf_online_school"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="${APP_HOME}/.venv/bin:$PATH"
RUN apt-get update && apt-get install -y postgresql-client

# Установка пакетов, необходимых для работы Django
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        musl-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Django
RUN pip install django

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем celery
RUN pip install --no-cache-dir celery

# Копируем файлы проекта
COPY . .

# Создаем виртуальное окружение и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "drf_online_school.wsgi"]
