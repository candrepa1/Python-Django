from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    phone_number = models.IntegerField()
