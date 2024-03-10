# materials/tasks.py

from celery import shared_task


@shared_task
def example_task():
    # Ваш код задачи здесь
    pass
