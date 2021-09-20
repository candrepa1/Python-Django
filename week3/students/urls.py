from django.urls import path

from students.views import StudentsListView, StudentDetailView

app_name = 'students'
urlpatterns = [
    path('', StudentsListView.as_view(), name='student-list'),
    path('<pk>/', StudentDetailView.as_view(), name='student-detail')
]