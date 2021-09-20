from django.shortcuts import render

from django.views.generic import ListView
from classes.models import Class


# Create your views here.
class ClassesListView(ListView):
    model = Class
    context_object_name = 'classes'
