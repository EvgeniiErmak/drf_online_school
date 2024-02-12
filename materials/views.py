# materials/views.py
from django.views.generic.base import TemplateView
from rest_framework import generics, viewsets
from .models import Course, Lesson, Payment  # Добавляем импорт модели Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer  # Добавляем импорт сериализатора PaymentSerializer


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


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация по курсу
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Фильтрация по уроку
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)

        # Фильтрация по способу оплаты
        payment_method = self.request.query_params.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        # Меняем порядок сортировки по дате оплаты
        queryset = queryset.order_by('-payment_date')

        return queryset
