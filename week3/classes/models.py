from django.db import models


# Create your models here.
class Class(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    teacher = models.CharField(max_length=200)
