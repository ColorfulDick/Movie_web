# Generated by Django 2.0.7 on 2020-02-11 08:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20200120_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 11, 16, 4, 28, 572578), verbose_name='发送时间'),
        ),
    ]
