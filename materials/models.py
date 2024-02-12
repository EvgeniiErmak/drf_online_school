# materials/models.py
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    description = models.TextField()


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)


class Payment(models.Model):
    # Добавляем related_name, чтобы устранить конфликт
    course = models.ForeignKey(Course, related_name='payments', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='payments', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255)
