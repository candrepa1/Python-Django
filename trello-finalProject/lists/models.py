import datetime

from django.db import models
from boards.models import Board

# Create your models here.


class List(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, related_name='lists', on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    position = models.IntegerField()

    def __str__(self):
        return self.name
