from django.db import models
from boards.models import Board


# Create your models here.

class Invitation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    accepted = models.BooleanField(default=False)
    board = models.ForeignKey(Board, related_name='invitation_board', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
