import datetime
from copy import copy
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lists.models import List
from lists.permissions import ListPermission
from lists.serializer import ListSerializer

# Create your views here.


class ListViewSet(ModelViewSet):
    """
        List endpoint

        change_position:
            Changes the position of a list in the board and returns the list's serialized data

        create:
            Creates a new List object and returns the serialized request data
    """
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (ListPermission, )

    def create(self, request, *args, **kwargs):
        position = 0
        data = copy(request.data)
        position_length = len(self.get_queryset())
        if position_length > 0:
            position = position_length
        data['position'] = position
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(methods=['PATCH'], detail=True)
    def change_position(self, request, pk):
        position = request.data['position']
        to_change = self.queryset.get(id=pk)
        in_position = self.queryset.get(position=position, board_id=to_change.board_id)
        to_change.position = position
        in_position.position = to_change.position
        in_position.save()
        to_change.save()
        serializer = self.get_serializer(to_change)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

