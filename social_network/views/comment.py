from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView
from social_network.forms.comment import CommentForm
from social_network.models import Comments, UserInfo


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    template_name = 'comment/comment_add.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post})

    def form_valid(self, form):
        form.instance.user_nickname = UserInfo.objects.get(user=self.request.user)
        return super().form_valid(form)
