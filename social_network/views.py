from django.views.generic import ListView
from social_network.models import *


class PostList(ListView):
    queryset = Post.objects.all()
    model = Post
    template_name = 'post.html'


class UserInfoListView(ListView):
    model = UserInfo
    template_name = 'users.html'
