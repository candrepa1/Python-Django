from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from teachers.models import Teacher
from teachers.permissions import TeacherPermission
from teachers.serializer import TeacherDetailSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailSerializer
    permission_classes = (TeacherPermission, )

    @action(methods=['GET'], detail=False)
    def order_by_name(self, request):
        ordered_names = self.queryset.order_by('name')
        serialized = self.get_serializer(ordered_names, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    def get_queryset(self):
        filter = {}
        for param in self.request.query_params:
            filter[param] = self.request.query_params[param]
        return self.queryset.filter(**filter)

