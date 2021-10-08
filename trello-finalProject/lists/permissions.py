from rest_framework.permissions import BasePermission

from boards.models import Board


class ListPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user_is_member = Board.objects.filter(id=request.data['board'], members__in=[request.user.id])
            if len(user_is_member) == 0:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'update':
            user_is_owner = Board.objects.filter(id=obj.board_id)
            if request.user.id == user_is_owner[0].owner_id:
                return True
            return False
        return True
