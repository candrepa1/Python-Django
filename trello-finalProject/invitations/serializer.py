from rest_framework.serializers import ModelSerializer
from invitations.models import Invitation


class InvitationSerializer(ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['name', 'email', 'accepted', 'board']