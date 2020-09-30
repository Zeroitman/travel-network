from django.urls import reverse
from django.views.generic import CreateView
from social_network.forms.comment import CommentForm
from social_network.models import Comments


class CommentCreateView(CreateView):
    model = Comments
    template_name = 'comment/comment_add.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post})

