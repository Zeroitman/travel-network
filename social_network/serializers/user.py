from rest_framework import serializers
from social_network.models import UserInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ()
