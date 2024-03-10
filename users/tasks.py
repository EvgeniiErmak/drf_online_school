# users/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import CustomUser


@shared_task
def lock_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = CustomUser.objects.filter(last_login__lte=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
