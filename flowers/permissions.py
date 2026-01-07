from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Админ может делать CRUD.
    Зарегистрированный пользователь: только чтение (GET, HEAD, OPTIONS).
    Анонимный: доступ только к GET, без изменений.
    """

    def has_permission(self, request, view):
        # Анонимный пользователь
        if not request.user or not request.user.is_authenticated:
            # Только GET запросы
            return request.method in permissions.SAFE_METHODS

        # Админ может всё
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Зарегистрированный пользователь: только чтение
        return request.method in permissions.SAFE_METHODS
