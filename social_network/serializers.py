from rest_framework import serializers
from social_network.models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        exclude = ()
