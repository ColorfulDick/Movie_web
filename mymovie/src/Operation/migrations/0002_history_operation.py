# Generated by Django 2.0.7 on 2020-02-11 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20200211_1604'),
        ('Movies', '0001_initial'),
        ('Operation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History_Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movies.movie', to_field='moviename', verbose_name='电影')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.User', to_field='username', verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '浏览历史',
                'verbose_name': '浏览历史',
            },
        ),
    ]
