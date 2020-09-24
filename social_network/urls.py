from django.urls import path
from social_network.views import PostList, UserListView, UserDetailView, change_access_status, change_create_post_status

urlpatterns = [
    path('post-list', PostList.as_view(), name='post_list'),
    path('users-list/', UserListView.as_view(), name='users_list'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/change_access_status', change_access_status, name='change_access_status'),
    path('user/<int:pk>/change_create_post_status', change_create_post_status, name='change_create_post_status'),
]
