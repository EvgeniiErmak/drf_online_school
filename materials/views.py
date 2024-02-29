# materials/views.py
from .models import Course, Lesson, Payment, Subscription
from django.views.generic.base import TemplateView
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, permissions, viewsets, status
from users.permissions import IsModerator, IsOwner
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """ Права доступа для ViewSet Course"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [permissions.IsAuthenticated | IsModerator]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        new_course = serializer.save()
        new_course.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.owner != self.request.user and not IsModerator().has_object_permission(self.request, self, instance):
            raise PermissionDenied("У вас нет прав на редактирование этого курса.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("У вас нет разрешения на удаление этого курса.")
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticated]  # Обновлено для получения деталей курса
        return super().retrieve(request, *args, **kwargs)


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        new_lesson = serializer.save()
        new_lesson.save()


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.owner != self.request.user and not IsModerator().has_object_permission(self.request, self, instance):
            raise PermissionDenied("У вас нет прав на редактирование этого урока.")
        serializer.save()


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("У вас нет разрешения на удаление этого урока.")
        instance.delete()


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        else:
            return [permissions.IsAuthenticated, IsModerator | IsOwner]

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


class HomeView(TemplateView):
    template_name = 'materials/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте здесь любые необходимые данные для передачи в шаблон
        return context


class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'detail': 'Необходимо указать ID курса'}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response({'detail': 'Курс с указанным ID не найден'}, status=status.HTTP_404_NOT_FOUND)

        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
        if created:
            message = 'Подписка на курс успешно создана'
        else:
            message = 'Вы уже подписаны на этот курс'

        return Response({'detail': message})

    def destroy(self, request, pk=None):
        subscription = Subscription.objects.filter(user=request.user, course_id=pk).first()
        if not subscription:
            return Response({'detail': 'Подписка на курс с указанным ID не найдена'}, status=status.HTTP_404_NOT_FOUND)

        subscription.delete()
        return Response({'detail': 'Подписка на курс успешно отменена'})
