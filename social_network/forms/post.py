from django import forms
from social_network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_subject', 'post_body', 'post_country', 'tag', 'image']
