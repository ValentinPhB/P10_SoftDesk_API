from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS only to non-admin users.
    """

    def has_permission(self, request, view):
        return bool((request.method
                     in permissions.SAFE_METHODS
                     or request.user and request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
