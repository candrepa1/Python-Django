import datetime

from factory import faker
from factory.django import DjangoModelFactory

from boards.models import Board


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    name = faker.Faker('name')
    description = faker.Faker('paragraph')
    creation_date = datetime.datetime.now()
