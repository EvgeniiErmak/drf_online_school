# Dockerfile

# Use the official Python image
FROM python:3.11-slim

# Set the environment variable for the working directory
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Set dependencies
ENV PYTHONPATH "${APP_HOME}:${APP_HOME}/drf_online_school"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="${APP_HOME}/.venv/bin:$PATH"

# Install necessary packages for Django and Celery
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        musl-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Django dependencies
RUN pip install django

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install Celery
RUN pip install --no-cache-dir celery

# Install Stripe
RUN pip install --no-cache-dir stripe

# Copy project files
COPY . .

# Create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Expose the port for the application
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "drf_online_school.wsgi"]
