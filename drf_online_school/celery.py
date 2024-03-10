# drf_online_school/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка переменной окружения с именем файла настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_online_school.settings')

# Создание экземпляра приложения Celery
app = Celery('drf_online_school')

# Использование файла настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическая настройка поиска задач в приложениях Django
app.autodiscover_tasks()
