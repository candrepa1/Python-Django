from copy import copy

from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from students.models import Student
from students.permissions import StudentPermission
from students.serializer import StudentDetailSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    permission_classes = (StudentPermission, )

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail(
            subject='Welcome to school!',
            message=f"Hi {request.data['name']}! "
                    f"Welcome to school, we are glad to have you here.",
            from_email='school@school.com',
            recipient_list=[request.data['email']]
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

