# Generated by Django 2.2.24 on 2021-10-08 01:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20211003_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 8, 1, 45, 42, 308959)),
        ),
    ]
