from django.urls import path
from social_network.views import PostList, UserListView, UserDetailView

urlpatterns = [
    path('post-list', PostList.as_view(), name='post_list'),
    path('users-list/', UserListView.as_view(), name='users_list'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user_detail'),

]
