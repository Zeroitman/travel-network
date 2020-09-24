from django.urls import path
from social_network.views import *

urlpatterns = [
    path('post-list', PostList.as_view(), name='post_list'),
    path('users-list', UserInfoListView.as_view(), name='user_list')
]
