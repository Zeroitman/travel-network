from rest_framework import serializers
from social_network.models import UserInfo, Post


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, i):
        data = super().to_representation(i)
        users_posts = [a.id for a in Post.objects.filter(post_user=i.id).order_by('post_country')]
        data['users_posts_id'] = users_posts
        return data

    class Meta:
        model = UserInfo
        fields = ("id", "full_name", "create_post_status", "access_status")
