# Generated by Django 4.0 on 2022-01-10 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='answers',
        ),
    ]
