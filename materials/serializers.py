# materials/serializers.py
from rest_framework import serializers
from .models import Course, Lesson, Payment
from .validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_video_link])  # добавляем валидатор

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'preview', 'description', 'course', 'video_link']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def validate_video_link(self, value):
        validate_video_link(value)
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
