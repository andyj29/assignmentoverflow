# Generated by Django 4.0 on 2022-01-14 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('networking', '0003_alter_connectrequest_sender_connectnotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectrequest',
            name='sender',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='connect_requests', to='authentication.user'),
        ),
    ]