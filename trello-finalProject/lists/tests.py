from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from boards.factories import BoardFactory
from boards.models import Board
from lists.factories import ListFactory
from lists.models import List


# Create your tests here.


class ListTestCase(APITestCase):
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

    def test_get_lists(self):
        response = self.client.get(f'{self.host}/lists/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()[0]
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(data['position'], 0)
        self.assertEqual(data['board'], 1)

    def test_get_list(self):
        response = self.client.get(f'{self.host}/lists/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['position'], 0)
        self.assertEqual(data['board'], 1)

    def test_create_list(self):
        self.board.members.add(self.user)
        data = {
            'name': 'from-testing',
            'board': 1,
        }
        response = self.client.post(f'{self.host}/lists/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['board'], data['board'])
        self.assertEqual(response_data['position'], 1)
        list_created = List.objects.filter(name=data['name'], board=1)
        self.assertEqual(len(self.lists), 2)
        self.assertEqual(len(list_created), 1)

    def test_update_list(self):
        data = {"name": "random-list-name"}
        response = self.client.patch(f'{self.host}/lists/1/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        list_updated = List.objects.filter(name=data['name']).values('name')
        self.assertEqual(list(list_updated)[0]['name'], data['name'])

    def test_delete_list(self):
        response = self.client.delete(f'{self.host}/lists/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.lists), 0)

    def test_change_position(self):
        self.board.members.add(self.user)
        data = {
            'name': 'from-testing',
            'board': 1,
            "position": 1
        }
        self.client.post(f'{self.host}/lists/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        position = {"position": 1}
        response = self.client.patch(f'{self.host}/lists/1/change_position/', data=position, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data_response = response.json()
        self.assertEqual(data_response['position'], 1)
        list_changed = List.objects.filter(id=1).values('position')
        self.assertEqual(list_changed[0]['position'], 1)
