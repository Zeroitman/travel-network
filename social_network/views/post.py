from django.views.generic import ListView
from social_network.models import Post


class PostList(ListView):
    queryset = Post.objects.all()
    model = Post
    template_name = 'post.html'
    permission_required = 'webapp.view_child'
