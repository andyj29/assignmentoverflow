# Generated by Django 4.0 on 2022-01-10 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('websocketchat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsession',
            name='initiator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='started_chat_session', to='authentication.user'),
        ),
        migrations.AlterField(
            model_name='chatsession',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participated_chat_session', to='authentication.user'),
        ),
    ]
