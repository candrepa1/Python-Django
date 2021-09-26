from rest_framework.serializers import ModelSerializer

from teachers.models import Teacher


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name']


class TeacherDetailSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
