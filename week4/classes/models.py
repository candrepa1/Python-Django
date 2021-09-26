from django.db import models


# Create your models here.
from students.models import Student
from teachers.models import Teacher


class Class(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, related_name='classes', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        return self.title
