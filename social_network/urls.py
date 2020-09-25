from django.urls import path
from social_network.views import \
    (PostList, PostCreateView, PostDetailView, change_post_status, increase_post_rating, decrease_post_rating,
     UserListView, UserDetailView,
     change_access_status, change_create_post_status)

urlpatterns = [
    path('post-list', PostList.as_view(), name='post_list'),
    path('post-create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/detail', PostDetailView.as_view(), name='post_detail'),
    path('post/<str:pk>/change_post_status', change_post_status, name='change_post_status'),
    path('post/<str:pk>/increase_post_rating', increase_post_rating, name='increase_post_rating'),
    path('post/<str:pk>/decrease_post_rating', decrease_post_rating, name='decrease_post_rating'),
    path('users-list/', UserListView.as_view(), name='users_list'),
    path('user/<int:pk>/detail', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/change_access_status', change_access_status, name='change_access_status'),
    path('user/<int:pk>/change_create_post_status', change_create_post_status, name='change_create_post_status'),
]
