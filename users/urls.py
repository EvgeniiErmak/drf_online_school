# users/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserProfileViewSet

app_name = 'users'

# Создаем экземпляр DefaultRouter
router = DefaultRouter()

# Регистрируем UserProfileViewSet под именем 'user-profile'
router.register(r'user-profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('user-profile/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-profile'),
    path('user-profile/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-profile-detail'),
    path('register/', UserProfileViewSet.as_view({'post': 'register'}), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
