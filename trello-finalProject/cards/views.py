import datetime
from copy import copy

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cards.models import Card
from cards.permissions import CardPermission
from cards.serializer import CardSerializer
from cards.tasks import notification_email, deadline_email

# Create your views here.


class CardViewSet(ModelViewSet):
    """
        Card endpoint

        add_members:
            Receives an array with the ids of the members to add to the card detail, adds them to the card members, and returns the serialized request data

        create:
            Creates a new Card object and returns the serialized request data
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (CardPermission, )

    def create(self, request, *args, **kwargs):
        position = 0
        data = copy(request.data)
        data['owner'] = request.user.id
        position_length = len(self.get_queryset())
        if position_length > 0:
            position = position_length
        data['position'] = position
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        card = self.queryset.last()
        eta = card.expiration_date - datetime.timedelta(days=1)
        deadline_email.apply_async(args=[card.id], eta=eta)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(methods=['PATCH'], detail=True)
    def add_members(self, request, pk):
        card = self.queryset.get(id=pk)
        all_members = []
        for member in request.data['members']:
            member_info = User.objects.filter(id=member)
            if len(member_info) == 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            card.members.add(member)
            all_members.append(member_info[0].email)
        notification_email.apply_async(args=[all_members, card.name])
        serializer = self.get_serializer(card)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


