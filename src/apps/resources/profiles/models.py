import uuid
from django.db import models
from django.utils import timezone


class Profile(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user = models.OneToOneField('authentication.User', related_name='profile', on_delete=models.CASCADE, editable=False)
	name = models.CharField(max_length=255, blank=True, null=True)
	email = models.EmailField(max_length=255, unique=True, editable=False)
	location = models.CharField(max_length=255, blank=True, null=True)
	intro = models.CharField(max_length=255, blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	image = models.ImageField(default=None, upload_to='profiles/', blank=True, null=True)
	github = models.CharField(max_length=255, blank=True, null=True)
	linkedin = models.CharField(max_length=255, blank=True, null=True)
	date_joined = models.DateTimeField(default=timezone.now, editable=False)
	follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

	def __str__(self):
		return self.user.username

