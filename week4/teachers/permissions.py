from rest_framework.permissions import BasePermission


class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create' and not request.user.is_superuser or view.action == 'update' and not request.user.is_superuser or view.action == 'destroy' and not request.user.is_superuser:
            return False

        return True
