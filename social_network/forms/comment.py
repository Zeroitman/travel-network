from django import forms
from social_network.models import Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['post', 'text']
