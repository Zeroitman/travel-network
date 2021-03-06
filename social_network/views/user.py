from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from social_network.forms.user import UserInfoForm, UserForm
from social_network.models import UserInfo, Post
from social_network.serializers.user import UserSerializer
from source.constants import API_SECURE_KEY
from source.utils import MediaResponse


class UserListView(LoginRequiredMixin, ListView):
    model = UserInfo
    template_name = 'user/users_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users_posts = {}
        for a in UserInfo.objects.all():
            users_posts[a.pk] = len(Post.objects.filter(post_user=a.pk))
        context['post_count'] = users_posts
        users_country = {}
        for a in UserInfo.objects.all():
            country = []
            users_country[a.pk] = 0
            for aa in Post.objects.filter(post_user=a.pk):
                country.append(aa.post_country)
                users_country[a.pk] = len(list(set(country)))
        context['users_country'] = users_country
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = UserInfo
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_pk = int(self.kwargs.get('pk'))
        current_user = UserInfo.objects.get(id=now_pk)
        context['current_user'] = current_user
        context['users_posts'] = Post.objects.filter(post_user=current_user).order_by('post_country')
        return context


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        p_form = UserInfoForm(request.POST)
        if form.is_valid() and p_form.is_valid():
            user = form.save()
            user.save()
            profile = p_form.save(commit=False)
            profile.user_id = user.pk
            profile.save()
            group = form.cleaned_data.pop('groups')
            for user_group in group:
                user.groups.add(user_group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} успешно зарегистрирован')
            return redirect('user_detail', pk=profile.pk)
        else:
            messages.info(request, f'Ошибка регистрации')
    else:
        form = UserForm()
        p_form = UserInfoForm()
    return render(request, 'registration.html', {'form': form, 'p_form': p_form})


@api_view(['GET'])
def users(request):
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(UserInfo.objects.all(), many=True)
    if serializer.data:
        return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)


@api_view(['GET'])
def user(request, pk):
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(UserInfo.objects.filter(pk=pk).first())
    if serializer.data:
        return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)
    return MediaResponse("FAIL", details="NO_DATA", code=status.HTTP_200_OK, result=[])


def change_access_status(request, pk):
    if request.user.is_superuser:
        user = get_object_or_404(UserInfo, pk=pk)
        user.access_status = False if user.access_status else True
        user.save()
    return redirect('users_list')
