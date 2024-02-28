# materials/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListView, LessonCreateView, LessonRetrieveView, LessonUpdateView, LessonDestroyView, HomeView, PaymentListCreateView

app_name = 'materials'

# Создаем экземпляр DefaultRouter
router = DefaultRouter()

# Регистрируем CourseViewSet под именем 'courses'
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/destroy/', LessonDestroyView.as_view(), name='lesson-destroy'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),

    # Включаем роутер в urlpatterns
    path('', include(router.urls)),
]
