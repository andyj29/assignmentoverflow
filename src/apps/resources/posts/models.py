import uuid
from django.db import models


class Post(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	author = models.ForeignKey('authentication.User', on_delete=models.CASCADE, editable=False)
	title = models.CharField(max_length=255)
	content = models.TextField()
	tags = models.ManyToManyField('Tag', blank=True)
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.author)


class Comment(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	author = models.ForeignKey('authentication.User', on_delete=models.CASCADE, editable=False)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, editable=False)
	content = models.TextField()
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.author)


class Tag(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	name = models.CharField(max_length=255, unique=True)
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name