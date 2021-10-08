from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from boards.factories import BoardFactory
from boards.models import Board
from cards.factories import CardFactory
from cards.models import Card
from comments.factories import CommentFactory
from comments.models import Comment
from invitations.factories import InvitationFactory
from invitations.models import Invitation
from lists.factories import ListFactory
from lists.models import List

# Create your tests here.


class InvitationTestCase(APITestCase):
    def setUp(self):
        self.host = 'http://127.0.0.1:8000'

        # register
        register_response = self.client.post(f'{self.host}/register/', {
            "first_name": "user4",
            "last_name": "last_name4",
            "email": "user4@test.com",
            "username": "username4",
            "password": "user4pwd"
        })
        assert register_response.status_code == 201
        self.user = User.objects.get(username='username4')

        # login
        login_response = self.client.post(f'{self.host}/api/token/', {
            'username': 'username4', 'password': 'user4pwd'
        })
        assert login_response.status_code == 200
        self.token = login_response.json().get('access')
        assert self.token

        # boards
        self.board = BoardFactory.create(owner=self.user)
        self.boards = Board.objects.all()

        # lists
        self.list = ListFactory.create()
        self.lists = List.objects.all()

        # cards
        self.card = CardFactory.create()
        self.cards = Card.objects.all()

        # comments
        self.comment = CommentFactory.create()
        self.comments = Comment.objects.all()

        # invitations
        self.invitation = InvitationFactory.create()
        self.invitations = Invitation.objects.all()

    def test_get_invitations(self):
        response = self.client.get(f'{self.host}/invitations/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()[0]
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(data['board'], 1)

    def test_get_invitation(self):
        response = self.client.get(f'{self.host}/invitations/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['board'], 1)

    def test_create_invitation(self):
        data = {
            "name": "test-invitation",
            "email": "test-invitation@test.com",
            "board": 1
        }
        response = self.client.post(f'{self.host}/invitations/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['email'], data['email'])
        self.assertEqual(response_data['board'], data['board'])
        invitation_created = Invitation.objects.filter(email=data['email'])
        self.assertEqual(len(self.invitations), 2)
        self.assertEqual(len(invitation_created), 1)

    def test_update_invitation(self):
        data = {"name": "random-invitation-name"}
        response = self.client.patch(f'{self.host}/invitations/1/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        invitation_updated = Invitation.objects.filter(name=data['name'], id=1).values('name')
        self.assertEqual(list(invitation_updated)[0]['name'], data['name'])

    def test_delete_invitation(self):
        response = self.client.delete(f'{self.host}/invitations/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.invitations), 0)

    def test_accept_invitation(self):
        response = self.client.post(f'{self.host}/invitations/1/accept_invitation/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        invitation = self.invitations.filter(id=1)
        self.assertTrue(invitation[0].accepted)