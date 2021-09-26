from rest_framework.permissions import BasePermission


class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff:
            return False

        if view.action == 'create' and not request.user.is_superuser or view.action == 'update' and not request.user.is_superuser or view.action == 'destroy' and not request.user.is_superuser:
            return False

        return True
