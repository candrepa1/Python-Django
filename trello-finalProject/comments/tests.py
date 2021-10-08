from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from boards.factories import BoardFactory
from boards.models import Board
from cards.factories import CardFactory
from cards.models import Card
from comments.factories import CommentFactory
from comments.models import Comment
from lists.factories import ListFactory
from lists.models import List

# Create your tests here.


class CommentTestCase(APITestCase):
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

    def test_get_comments(self):
        response = self.client.get(f'{self.host}/comments/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()[0]
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(data['card'], 1)
        self.assertEqual(data['owner'], 1)

    def test_get_comment(self):
        response = self.client.get(f'{self.host}/comments/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['card'], 1)
        self.assertEqual(data['owner'], 1)

    def test_create_comment(self):
        data = {"message": "random-comment-message", "card": 1}
        response = self.client.post(f'{self.host}/comments/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['message'], data['message'])
        self.assertEqual(response_data['card'], data['card'])
        comment_created = Comment.objects.filter(message=data['message'], card=1)
        self.assertEqual(len(self.comments), 2)
        self.assertEqual(len(comment_created), 1)

    def test_update_comment(self):
        data = {"message": "random-comment-message"}
        response = self.client.patch(f'{self.host}/comments/1/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        comment_updated = Comment.objects.filter(message=data['message'], id=1).values('message')
        self.assertEqual(list(comment_updated)[0]['message'], data['message'])

    def test_delete_comment(self):
        response = self.client.delete(f'{self.host}/comments/1/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.comments), 0)
