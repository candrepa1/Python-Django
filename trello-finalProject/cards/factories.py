import datetime

from factory import faker
from factory.django import DjangoModelFactory

from cards.models import Card


class CardFactory(DjangoModelFactory):
    class Meta:
        model = Card

    name = faker.Faker('name')
    list_id = 1
    description = faker.Faker('paragraph')
    owner_id = 1
    creation_date = datetime.datetime.now()
    expiration_date = "2021-10-10T15:41:30.069843Z"
    position = 0
