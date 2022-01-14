# Generated by Django 4.0 on 2022-01-14 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('networking', '0004_alter_connectrequest_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectrequest',
            name='receiver',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='connect_invites', to='authentication.user'),
        ),
    ]
