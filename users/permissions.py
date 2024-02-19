# users/permissions.py
from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators to perform certain actions.
    """

    def has_permission(self, request, view):
        # Проверка, что пользователь является модератором
        return request.user.groups.filter(name='Модераторы').exists()
