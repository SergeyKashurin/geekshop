# Generated by Django 2.2.2 on 2019-07-01 09:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20190701_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 3, 9, 7, 1, 257134, tzinfo=utc)),
        ),
    ]
