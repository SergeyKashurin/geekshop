# Generated by Django 2.2.2 on 2019-07-01 07:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 3, 7, 10, 19, 645723, tzinfo=utc)),
        ),
    ]
