# users/permissions.py
from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators to perform certain actions.
    """

    def has_permission(self, request, view):
        # Проверка, что пользователь является модератором и метод запроса не безопасный
        return request.user.groups.filter(name='Модераторы').exists() and not request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        # Проверка, что пользователь является владельцем объекта
        return obj.owner == request.user or request.user.groups.filter(name='Пользователи').exists()

