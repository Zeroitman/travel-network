from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from social_network.models import UserInfo


class UserForm(UserCreationForm):
    error_css_class = 'text-danger small font-weight-light d-block'
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.Select
                                            (attrs={'class': 'form-control form-control-sm shadow-none'}),
                                            required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-sm shadow-none',
                       'placeholder': 'Логин пользователя'}),
            'password1': forms.PasswordInput(
                attrs={'style': 'form-control form-control-sm shadow-none',
                       'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(
                attrs={'class': 'form-control form-control-sm shadow-none',
                       'placeholder': 'Подтверждение пароля'})
        }


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(
                attrs={'class': 'form-control form-control-sm shadow-none',
                       'placeholder': 'Контакты'}),
        }


