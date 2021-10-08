import datetime

from factory import faker
from factory.django import DjangoModelFactory

from lists.models import List


class ListFactory(DjangoModelFactory):
    class Meta:
        model = List

    name = faker.Faker('name')
    creation_date = datetime.datetime.now()
    board_id = 1
    position = 0
