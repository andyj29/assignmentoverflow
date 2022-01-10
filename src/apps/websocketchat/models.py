import uuid
from django.db import models


class ChatSession(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	initiator = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, related_name='started_chat_session', null=True)
	receiver = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, related_name='participated_chat_session', null=True)
	created = models.DateTimeField(auto_now_add=True, editable=False)


class Message(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='session_messages', editable=False)
	sender = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, related_name='sent_messages', null=True, editable=False)
	text = models.TextField()
	attachment = models.FileField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-timestamp',)
