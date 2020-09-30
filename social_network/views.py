from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from social_network.forms import UserInfoForm, UserForm, PostForm
from social_network.models import Post, UserInfo
from social_network.serializers import PostSerializer, UserSerializer
from source.constants import API_SECURE_KEY
from source.utils import MediaResponse


class PostList(ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(activity=True)


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object})


class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post
    template_name = 'post_detail.html'


class UserListView(ListView, LoginRequiredMixin):
    model = UserInfo
    template_name = 'users_list.html'


class UserDetailView(DetailView, LoginRequiredMixin):
    model = UserInfo
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_pk = int(self.kwargs.get('pk'))
        current_user = UserInfo.objects.get(id=now_pk)
        context['current_user'] = current_user
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


def change_access_status(request, pk):
    if request.user.is_superuser:
        user = get_object_or_404(UserInfo, pk=pk)
        user.access_status = False if user.access_status else True
        user.save()
    return redirect('users_list')


def change_create_post_status(request, pk):
    if request.user.is_superuser:
        user = get_object_or_404(UserInfo, pk=pk)
        user.create_post_status = False if user.create_post_status else True
        user.save()
    return redirect('users_list')


def change_post_status(request, pk):
    if request.user.is_superuser:
        post = get_object_or_404(Post, pk=pk)
        post.activity = False if post.activity else True
        post.save()
    return redirect('post_list')


@api_view(['POST', 'GET'])
def post(request):
    # if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
    #     return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        user_id = request.data.get('post_user')
        user = User.objects.filter(pk=user_id).first()
        if user:
            if user.is_superuser:
                return MediaResponse("FAIL", "ADMIN_CAN'T_CREATE_POST", code=status.HTTP_200_OK)
            new_request_data = request.data.copy()
            new_request_data['activity'] = True
            serializer = PostSerializer(data=new_request_data)
            if serializer.is_valid():
                serializer.save()
                return MediaResponse("SUCCESS", "SUCCESSFULLY_ADDED", code=status.HTTP_200_OK)
            return MediaResponse("FAIL", serializer.errors, code=status.HTTP_200_OK)
    else:
        posts = Post.objects.filter(activity=True)
        serializer = PostSerializer(posts, many=True)
        if serializer.data:
            return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)
    return MediaResponse("SUCCESS", details="NO_DATA", code=status.HTTP_200_OK, result=[])


@api_view(['GET'])
def users(request):
    # if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
    #     return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(UserInfo.objects.all(), many=True)
    if serializer.data:
        return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)


def change_rating(request, pk, up=True):
    if not request.user.is_superuser and request.user:
        post = get_object_or_404(Post, pk=pk)
        if up:
            post.rating += 1
        else:
            post.rating -= 1
        post.save()
        return True
    return False


def increase_post_rating(request, pk):
    change_rating(request, pk)
    return redirect('post_list')


def decrease_post_rating(request, pk):
    change_rating(request, pk, False)
    return redirect('post_list')


@api_view(['POST'])
def api_increase_post_rating(request, pk):
    # if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
    #     return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    if change_rating(request, pk):
        return MediaResponse("SUCCESS", "RATINGS_INCREASED", code=status.HTTP_200_OK)


@api_view(['POST'])
def api_decrease_post_rating(request, pk):
    print("Her")
    # if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
    #     return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    if change_rating(request, pk, False):
        return MediaResponse("SUCCESS", "RATINGS_DECREASED", code=status.HTTP_200_OK)
