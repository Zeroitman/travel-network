from django.urls import path
from social_network.views.post import PostList

urlpatterns = [
    path('list', PostList.as_view(), name='post_list')
]
