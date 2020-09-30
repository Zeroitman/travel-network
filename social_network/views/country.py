from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from social_network.forms.user import UserInfoForm, UserForm
from social_network.models import Country, Post
from social_network.serializers.user import UserSerializer
from source.utils import MediaResponse


# class UserListView(ListView, LoginRequiredMixin):
#     model = UserInfo
#     template_name = 'user/users_list.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         users_posts = {}
#         for a in UserInfo.objects.all():
#             users_posts[a.pk] = len(Post.objects.filter(post_user=a.pk))
#         context['post_count'] = users_posts
#         return context


class CountryDetailView(DetailView, LoginRequiredMixin):
    model = Country
    template_name = 'country/country_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_pk = int(self.kwargs.get('pk'))
        post_list = Post.objects.filter(post_country=now_pk).order_by('-created_date')
        context['post_list'] = post_list
        return context
