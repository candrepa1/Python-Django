import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    owner = models.ForeignKey(User, related_name='board_owner', on_delete=models.SET_NULL, null=True)
    favorite = models.ManyToManyField(User, related_name='board_favorite')
    visibility = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name='board_member')

    def __str__(self):
        return self.name
