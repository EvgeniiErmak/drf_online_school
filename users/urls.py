# users/urls.py
from django.urls import path
from .views import UserProfileViewSet

app_name = 'users'

urlpatterns = [
    path('user-profile/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-profile'),
    path('user-profile/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-profile-detail'),
]
