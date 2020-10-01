from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import status
from rest_framework.decorators import api_view
from social_network.forms.post import PostForm
from social_network.models import *
from social_network.serializers.post import PostSerializer
from source.utils import MediaResponse


class PostList(ListView):
    model = Post
    template_name = 'post/post_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(activity=True).order_by('created_date')


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'post/post_create.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object})

    def form_valid(self, form):
        form.instance.post_user = UserInfo.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post
    template_name = 'post/post_detail.html'


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


# ----------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def api_increase_post_rating(request, pk):
    if change_rating(request, pk):
        return MediaResponse("SUCCESS", "RATINGS_INCREASED", code=status.HTTP_200_OK)


@api_view(['POST'])
def api_decrease_post_rating(request, pk):
    if change_rating(request, pk, False):
        return MediaResponse("SUCCESS", "RATINGS_DECREASED", code=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def post(request):
    if request.method == 'POST':
        user_id = request.data.get('post_user')
        user = UserInfo.objects.filter(pk=user_id).first()
        if user:
            if not user.create_post_status:
                return MediaResponse("FAIL", "THIS_USER_CAN'T_CREATE_POST", code=status.HTTP_200_OK)
            new_request_data = request.data.copy()
            new_request_data['activity'] = True
            serializer = PostSerializer(data=new_request_data)
            if serializer.is_valid():
                serializer.save()
                return MediaResponse("SUCCESS", "SUCCESSFULLY_ADDED", code=status.HTTP_200_OK)
            return MediaResponse("FAIL", serializer.errors, code=status.HTTP_200_OK)
    else:
        posts = Post.objects.filter(activity=True).order_by('created_date')
        serializer = PostSerializer(posts, many=True)
        if serializer.data:
            return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)
    return MediaResponse("SUCCESS", details="NO_DATA", code=status.HTTP_200_OK, result=[])


@api_view(['GET'])
def get_post(request, pk):
    serializer = PostSerializer(Post.objects.filter(pk=pk, activity=True).first())
    if serializer.data:
        return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)
    return MediaResponse("FAIL", details="NO_DATA", code=status.HTTP_200_OK, result=[])
