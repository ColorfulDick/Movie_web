# Generated by Django 2.0.7 on 2020-02-27 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20200211_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 27, 20, 53, 14, 768436), verbose_name='发送时间'),
        ),
    ]
