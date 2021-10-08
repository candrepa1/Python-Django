from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lists.models import List


class ListSerializer(ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = List
        fields = ['name', 'creation_date', 'position', 'board']
