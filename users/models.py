# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
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

    def save(self, *args, **kwargs):
        # При сохранении нового пользователя добавляем его в группу "Пользователи"
        if not self.pk:  # Если пользователь новый
            group, created = Group.objects.get_or_create(name='Пользователи')
            self.groups.add(group)
        super().save(*args, **kwargs)
