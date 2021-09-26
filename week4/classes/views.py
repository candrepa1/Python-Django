from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from classes.models import Class
from classes.permissions import ClassPermission
from classes.serializer import ClassDetailSerializer
from students.serializer import StudentsSerializer


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassDetailSerializer
    permission_classes = (ClassPermission,)

    @action(methods=['GET'], detail=True)
    def show_students(self, request, pk):
        class_detail = Class.objects.get(id=pk)
        students = class_detail.students.all()
        serialized = StudentsSerializer(students, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(methods=['PATCH'], detail=True)
    def add_students(self, request, pk):
        class_detail = Class.objects.get(id=pk)
        for student in request.data['students']:
            class_detail.students.add(student)
        class_detail.save()
        serialized = ClassDetailSerializer(class_detail)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    @action(methods=['GET'], detail=False)
    def order_by_title(self, request):
        ordered_names = self.queryset.order_by('title')
        serialized = self.get_serializer(ordered_names, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    def get_queryset(self):
        filter = {}
        for param in self.request.query_params:
            filter[param] = self.request.query_params[param]
        return self.queryset.filter(**filter)
