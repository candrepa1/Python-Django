from rest_framework.serializers import ModelSerializer

from classes.models import Class


class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = ['title']


class ClassDetailSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
