import datetime
from copy import copy

from rest_framework import status
from rest_framework.response import Response

from comments.models import Comment
from comments.serializer import CommentSerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class CommentViewSet(ModelViewSet):
    """
            Comment endpoint

            create:
                Creates a new Comment object and returns the serialized request data
        """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        data = copy(request.data)
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


