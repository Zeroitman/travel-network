from django import forms
from social_network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_user', 'post_subject', 'post_body', 'tag', 'image']
