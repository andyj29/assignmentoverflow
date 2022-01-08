import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
	def _create_user(self, username, email, password, **extra_fields):
		if not username:
			raise ValueError('Username can\'t be empty')
		if not email:
			raise ValueError('Email can\'t be empty')
		username = self.model.normalize_username(username)
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True')

		return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	username = models.CharField(max_length=255, unique=True, editable=False)
	email = models.EmailField(max_length=255, unique=True, editable=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email



