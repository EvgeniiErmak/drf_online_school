# materials/admin.py
from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'moderator')  # ������������ ���� � ������
    search_fields = ('title', 'owner__email')  # ���� ��� ������
    list_filter = ('owner', 'moderator')  # �������


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'owner', 'moderator')  # ������������ ���� � ������
    search_fields = ('title', 'course__title', 'owner__email')  # ���� ��� ������
    list_filter = ('course', 'owner', 'moderator')  # �������
