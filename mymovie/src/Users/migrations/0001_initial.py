﻿# Generated by Django 2.0.7 on 2019-05-14 04:31

import Users.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '忘记密码')], max_length=20, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(default=datetime.datetime(2019, 5, 14, 12, 31, 38, 559552), verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=1, verbose_name='性别')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='邮箱')),
                ('area', models.CharField(max_length=15, verbose_name='地区')),
                ('createDate', models.DateTimeField(auto_now_add=True, verbose_name='创建该账号的时间')),
                ('loadDate', models.DateTimeField(auto_now=True, verbose_name='上次登录时间')),
                ('userip', models.GenericIPAddressField(verbose_name='用户登录ip')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=Users.models.User.get_photo, verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户列表',
                'verbose_name_plural': '用户列表',
            },
        ),
    ]
