# Generated by Django 4.0 on 2022-01-08 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_last_updated_alter_profile_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
