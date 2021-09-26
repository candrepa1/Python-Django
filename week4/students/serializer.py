from rest_framework.serializers import ModelSerializer

from students.models import Student


class StudentsSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email']


class StudentDetailSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
