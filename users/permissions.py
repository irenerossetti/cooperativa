from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permiso para administradores"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or 
            (request.user.role and request.user.role.name == 'ADMIN')
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso de lectura para todos, escritura solo para administradores"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or 
            (request.user.role and request.user.role.name == 'ADMIN')
        )
