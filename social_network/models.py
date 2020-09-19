from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class UserInfo(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='client', verbose_name='Пользователь')

    def __str__(self):
        return "%s" % self.user.username


class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_subject = models.CharField("Тема поста", max_length=200)
    post_body = models.TextField("Тело поста", validators=[MinLengthValidator(3)])
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Image(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def __str__(self):
        return str(self.id)
