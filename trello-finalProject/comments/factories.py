import datetime

from factory import faker
from factory.django import DjangoModelFactory

from comments.models import Comment


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    card_id = 1
    message = faker.Faker('paragraph')
    owner_id = 1
    creation_date = datetime.datetime.now()