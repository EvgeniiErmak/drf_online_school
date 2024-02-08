# users/views.py
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
