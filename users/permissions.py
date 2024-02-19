# users/permissions.py
from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators to perform certain actions.
    """

    def has_permission(self, request, view):
        # Проверка, что пользователь является модератором
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Custom permission to only allow owners or moderators to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        # Проверка, что пользователь является владельцем объекта или модератором
        return obj.user == request.user or request.user.groups.filter(name='Модераторы').exists()
