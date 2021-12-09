from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS only to admin users.
    """

    def has_permission(self, request, view):
        return bool((request.method
                     in permissions.SAFE_METHODS
                     or request.user and request.user.is_staff))
