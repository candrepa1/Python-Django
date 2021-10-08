import datetime

from django.contrib.auth.models import User
from django.db import models
from lists.models import List


# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=100)
    list = models.ForeignKey(List, related_name='cards', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(User, related_name='cards_member')
    owner = models.ForeignKey(User, related_name='cards_owner', on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    expiration_date = models.DateTimeField()
    position = models.IntegerField()

    def __str__(self):
        return self.name
