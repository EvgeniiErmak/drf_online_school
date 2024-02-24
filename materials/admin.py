# materials/admin.py
from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'moderator')  # Отображаемые поля в списке
    search_fields = ('title', 'owner__email')  # Поля для поиска
    list_filter = ('owner', 'moderator')  # Фильтры


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'owner', 'moderator')  # Отображаемые поля в списке
    search_fields = ('title', 'course__title', 'owner__email')  # Поля для поиска
    list_filter = ('course', 'owner', 'moderator')  # Фильтры
