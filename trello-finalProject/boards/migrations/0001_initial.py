# Generated by Django 2.2.24 on 2021-10-01 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('creation_date', models.DateTimeField()),
                ('visibility', models.BooleanField(default=False)),
                ('favorite', models.ManyToManyField(related_name='board_favorite', to='users.User')),
                ('members', models.ManyToManyField(related_name='board_member', to='users.User')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='board_owner', to='users.User')),
            ],
        ),
    ]
