# users/models.py
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson
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


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_date = models.DateField()
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )
    payment_method = models.CharField(max_length=10, choices=payment_method_choices)
