from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from cards.models import Card


class CardSerializer(ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Card
        fields = ['name', 'description', 'creation_date', 'expiration_date', 'position', 'list', 'owner']
