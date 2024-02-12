# materials/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, HomeView, PaymentListCreateView

app_name = 'materials'

# Создаем экземпляр DefaultRouter
router = DefaultRouter()

# Регистрируем CourseViewSet под именем 'courses'
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),

    # Включаем роутер в urlpatterns
    path('', include(router.urls)),
]
