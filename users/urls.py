# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

app_name = 'users'

# Создаем экземпляр DefaultRouter
router = DefaultRouter()

# Регистрируем UserProfileViewSet под именем 'user-profile'
router.register(r'user-profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
]
