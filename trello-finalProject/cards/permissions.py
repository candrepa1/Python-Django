from rest_framework.permissions import BasePermission

from boards.models import Board
from lists.models import List


class CardPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            board = List.objects.get(id=request.data['list']).board_id
            user_is_member = Board.objects.filter(id=board, members__in=[request.user.id])
            if len(user_is_member) == 0:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'update':
            board = List.objects.filter(id=obj.list_id)[0].board_id
            user_is_owner = Board.objects.filter(id=board)
            if request.user.id == user_is_owner[0].owner_id:
                return True
            return False
        return True
