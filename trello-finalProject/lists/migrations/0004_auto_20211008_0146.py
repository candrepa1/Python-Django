# Generated by Django 2.2.24 on 2021-10-08 01:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20211008_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 8, 1, 46, 11, 712227)),
        ),
    ]
