from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from users.serializer import UserSerializer

# Create your views here.


class UserViewSet(ModelViewSet):
    """
        Registration(User) endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )