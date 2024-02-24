# users/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer

User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
