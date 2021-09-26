from django.db import models


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name
