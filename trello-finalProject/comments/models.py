import datetime

from django.contrib.auth.models import User
from django.db import models
from cards.models import Card

# Create your models here.


class Comment(models.Model):
    card = models.ForeignKey(Card, related_name='comments', on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=300)
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.message
