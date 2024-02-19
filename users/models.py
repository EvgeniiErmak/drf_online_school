# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from materials.models import Course, Lesson
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, city, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, city=city, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, city, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, phone, city, password, **extra_fields)


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

    objects = CustomUserManager()


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
