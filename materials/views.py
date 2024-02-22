# materials/views.py
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Payment
from django.views.generic.base import TemplateView
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.permissions import IsModerator, IsOwnerOrModerator
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response


class HomeView(TemplateView):
    template_name = 'materials/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте здесь любые необходимые данные для передачи в шаблон
        return context


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsModerator]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Привязываем курс к пользователю-владельцу
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Добавляем метод удаления модератора курса
    def destroy_moderator(self, request, *args, **kwargs):
        course = self.get_object()
        course.moderator = None
        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]  # Пермишен для авторизованных пользователей

    # Определяем права доступа для разных методов
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsModerator]
        else:
            permission_classes = [IsOwnerOrModerator]
        return [permission() for permission in permission_classes]

    # Привязываем урок к пользователю-владельцу при создании
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]  # Пермишен для авторизованных пользователей

    # Определяем права доступа для разных методов
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsModerator]
        else:
            permission_classes = [IsOwnerOrModerator]
        return [permission() for permission in permission_classes]


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Пермишен для авторизованных пользователей

    # Определяем права доступа для разных методов
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsModerator]
        else:
            permission_classes = [IsOwnerOrModerator]
        return [permission() for permission in permission_classes]

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
