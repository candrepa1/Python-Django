from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from boards.factories import BoardFactory
from boards.models import Board
from cards.factories import CardFactory
from cards.models import Card
from lists.factories import ListFactory
from lists.models import List

# Create your tests here.


class CardTestCase(APITestCase):
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

        # self.user = User.objects.create_user(username='username4', email='user4@test.com', password='user4pwd')

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

    def test_get_cards(self):
        response = self.client.get(f'{self.host}/cards/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()[0]
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(data['position'], 0)
        self.assertEqual(data['list'], 1)
        self.assertEqual(data['owner'], 1)
        self.assertEqual(data['expiration_date'], "2021-10-10T15:41:30.069843Z")

    def test_get_card(self):
        response = self.client.get(f'{self.host}/cards/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['position'], 0)
        self.assertEqual(data['list'], 1)
        self.assertEqual(data['owner'], 1)
        self.assertEqual(data['expiration_date'], "2021-10-10T15:41:30.069843Z")

    def test_create_card(self):
        self.board.members.add(self.user)
        data = {
            'name': 'from-testing',
            'description': "testing description",
            "expiration_date": "2021-10-10T15:41:30.069843Z",
            "list": 1,
            "position": 1
        }
        response = self.client.post(f'{self.host}/cards/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['description'], data['description'])
        self.assertEqual(response_data['expiration_date'], "2021-10-10T15:41:30.069843Z")
        self.assertEqual(response_data['list'], data['list'])
        self.assertEqual(response_data['position'], data['position'])
        card_created = Card.objects.filter(name=data['name'], list=1)
        self.assertEqual(len(self.cards), 2)
        self.assertEqual(len(card_created), 1)

    def test_update_card(self):
        data = {"name": "random-card-name"}
        response = self.client.patch(f'{self.host}/cards/1/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        card_updated = Card.objects.filter(name=data['name']).values('name')
        self.assertEqual(list(card_updated)[0]['name'], data['name'])

    def test_delete_card(self):
        response = self.client.delete(f'{self.host}/cards/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.cards), 0)

    def test_add_members(self):
        data = {"members": [1]}
        response = self.client.patch(f'{self.host}/cards/1/add_members/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        members = self.cards[0].members.all()
        self.assertEqual(len(members), 1)
        self.assertIsInstance(members[0], User)
        self.assertEqual(members[0].id, 1)