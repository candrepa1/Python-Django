from copy import copy
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from boards.serializer import BoardSerializer
from boards.models import Board


# Create your views here.


class BoardViewSet(ModelViewSet):
    """
        Board endpoint

        create:
            Creates a new Board object and returns the serialized request data

        favorites:
            Returns an array with all the user's favorite boards

        add_to_favorites:
            Adds the user's id to the specified Board's favorites array
        """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        data = copy(request.data)
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def favorites(self, request):
        favorites = self.queryset.filter(members__in=[request.user.id])
        serializer = self.get_serializer(favorites, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['POST'], detail=True)
    def add_to_favorites(self, request, pk):
        board = self.get_object()
        board.favorite.add(request.user.id)
        board.save()
        serializer = self.get_serializer(board)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
