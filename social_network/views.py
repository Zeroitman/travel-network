from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from social_network.forms import UserInfoForm, UserForm, PostForm
from social_network.models import Post, UserInfo


class PostList(ListView):
    queryset = Post.objects.all()
    model = Post
    template_name = 'post_list.html'


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': 1})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class UserListView(ListView):
    model = UserInfo
    template_name = 'users_list.html'


class UserDetailView(DetailView):
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
    user = get_object_or_404(UserInfo, pk=pk)
    user.access_status = False if user.access_status else True
    user.save()
    return redirect('users_list')


def change_create_post_status(request, pk):
    user = get_object_or_404(UserInfo, pk=pk)
    user.create_post_status = False if user.create_post_status else True
    user.save()
    return redirect('users_list')
