from factory import faker
from factory.django import DjangoModelFactory

from invitations.models import Invitation


class InvitationFactory(DjangoModelFactory):
    class Meta:
        model = Invitation

    name = faker.Faker('name')
    email = 'user4@test.com'
    accepted = False
    board_id = 1
