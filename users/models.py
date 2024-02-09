# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Отключение поля username
    username = None

    # Установка email в качестве USERNAME_FIELD
    USERNAME_FIELD = 'email'
    # Обязательные поля, кроме email
    REQUIRED_FIELDS = ['phone', 'city']
