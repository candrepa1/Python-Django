from django.urls import path

from classes.views import ClassesListView

app_name = 'classes'
urlpatterns = [
    path('', ClassesListView.as_view(), name='classes-list'),
]