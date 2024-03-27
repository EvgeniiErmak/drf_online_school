# Dockerfile

# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменную среды для рабочей директории
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Устанавливаем зависимости
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y postgresql-client

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем команду для миграций
RUN python manage.py migrate

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "drf_online_school.wsgi"]
