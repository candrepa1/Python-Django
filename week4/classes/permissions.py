from rest_framework.permissions import BasePermission


class ClassPermission(BasePermission):

    def has_permission(self, request, view):

        if view.action == 'show_students' and not request.user.is_staff or view.action == 'add_students' and not request.user.is_staff:
            return False

        if view.action == 'create' and not request.user.is_superuser or view.action == 'destroy' and not request.user.is_superuser:
            return False

        return True
