# Generated by Django 2.1 on 2020-09-30 13:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100000, null=True, verbose_name='Текст комментария')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название страны')),
                ('capital', models.CharField(max_length=500, verbose_name='Столица')),
                ('region', models.CharField(max_length=500, verbose_name='Регион')),
                ('population', models.CharField(max_length=500, verbose_name='Население')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_subject', models.CharField(max_length=200, verbose_name='Тема поста')),
                ('post_body', models.TextField(validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Тело поста')),
                ('tag', models.CharField(blank=True, max_length=100, verbose_name='Тэги')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('activity', models.BooleanField(default=True, verbose_name='Активность')),
                ('rating', models.SmallIntegerField(default=0, verbose_name='Рейтинг поста')),
                ('post_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_network.Country', verbose_name='Страна поста')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО пользователя')),
                ('create_post_status', models.BooleanField(default=True, verbose_name='Возможность создавать посты')),
                ('access_status', models.BooleanField(default=True, verbose_name='Статус доступа к приложению')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='post_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_network.UserInfo', verbose_name='Создатель поста'),
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social_network.Post'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user_nickname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social_network.UserInfo'),
        ),
    ]
