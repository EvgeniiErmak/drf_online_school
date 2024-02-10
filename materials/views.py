# materials/views.py
from django.views.generic.base import TemplateView
from rest_framework import generics, viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class HomeView(TemplateView):
    template_name = 'materials/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте здесь любые необходимые данные для передачи в шаблон
        return context


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
