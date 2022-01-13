from django.db.models.signals import post_save
from django.dispatch import receiver
from src.apps.resources.profiles.models import Profile
from src.apps.networking.models import Network
from .models import User


@receiver(post_save, sender=User)
def generate_user_profile(sender, instance, created, *args, **kwargs):
	if instance and created:
		Profile.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def generate_user_network(sender, instance, created, *args, **kwargs):
	if instance and created:
		Network.objects.create(user=instance)
