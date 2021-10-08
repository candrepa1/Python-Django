from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from boards.models import Board
from invitations.models import Invitation
from invitations.serializer import InvitationSerializer
from invitations.tasks import invitation_email


# Create your views here.


class InvitationViewSet(ModelViewSet):
    """
        Invitation endpoint

        accept_invitation:
            Changes the accepted status to True and returns the invitation's serialized data

        create:
            Creates a new Invitation object and returns the serialized request data
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def create(self, request, *args, **kwargs):
        if self.queryset.filter(email=request.data['email'], board_id=request.data['board']):
            return Response(status=status.HTTP_226_IM_USED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        message = ''
        if User.objects.filter(email=request.data['email']):
            message = '<a href="http://127.0.0.1:8000/api/token/">Go to board</a>'
        else:
            message = '<a href="http://127.0.0.1:8000/register/">Register</a>'
        invitation_email.apply_async(args=[request.data, message])
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(methods=['POST'], detail=True)
    def accept_invitation(self, request, pk):
        invitation = self.queryset.get(id=pk)
        if request.user.email != invitation.email or invitation.accepted:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        invitation.accepted = True
        invitation.save()
        board = Board.objects.get(id=invitation.board_id)
        board.members.add(request.user.id)
        board.save()
        serializer = self.get_serializer(invitation)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
