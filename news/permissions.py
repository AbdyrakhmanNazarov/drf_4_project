from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Только админ может CRUD.
    Обычный пользователь и аноним не имеют прав.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
