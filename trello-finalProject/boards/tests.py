from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from boards.factories import BoardFactory
from boards.models import Board

# Create your tests here.


class BoardTestCase(APITestCase):
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

    def test_get_boards(self):
        response = self.client.get(f'{self.host}/boards/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['owner'], 1)

    def test_get_board(self):
        response = self.client.get(f'{self.host}/boards/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['owner'], 1)

    def test_create_board(self):
        data = {
            'name': 'from-testing',
            'description': 'testing description',
        }
        response = self.client.post(f'{self.host}/boards/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], data['name'])
        self.assertEqual(response_data['description'], data['description'])
        self.assertEqual(response_data['owner'], 1)
        board_created = Board.objects.filter(name=data['name'])
        self.assertEqual(len(self.boards), 2)
        self.assertEqual(len(board_created), 1)

    def test_update_board(self):
        data = {"name": "random-board-name"}
        response = self.client.patch(f'{self.host}/boards/1/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        board_updated = Board.objects.filter(name=data['name']).values('name')
        self.assertEqual(list(board_updated)[0]['name'], data['name'])

    def test_delete_board(self):
        response = self.client.delete(f'{self.host}/boards/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.boards), 0)

    def test_get_favorite_boards(self):
        self.board.favorite.set([self.user])
        response = self.client.get(f'{self.host}/boards/favorites/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # print(response.json(), 'JSON')
        # FIX
        self.assertEqual(response.status_code, 200)

    def test_add_to_favorites(self):
        response = self.client.post(f'{self.host}/boards/1/add_to_favorites/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        favorite = self.boards[0].favorite.all()[0]
        self.assertIsInstance(favorite, User)
        self.assertEqual(favorite.username, 'username4')

