# materials/models.py
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    description = models.TextField()
    moderator = models.ForeignKey(User, related_name='moderated_courses', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='owned_courses', on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    moderator = models.ForeignKey(User, related_name='moderated_lessons', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='owned_lessons', on_delete=models.CASCADE)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )
    payment_method = models.CharField(max_length=10, choices=payment_method_choices)
