"""
Кастомные классы прав доступа, для приложения `users`.
"""

from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверка наличия прав модератора"""

    def has_permission(self, request, view):
        """Проверка пользователя на наличие группы с разрешениями"""
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь создателем/владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
