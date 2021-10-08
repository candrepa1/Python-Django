from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from comments.models import Comment


class CommentSerializer(ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Comment
        fields = '__all__'
