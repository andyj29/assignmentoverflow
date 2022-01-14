import uuid
from django.db import models
from django.shortcuts import get_object_or_404


class Network(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user = models.OneToOneField('authentication.User', related_name='network', on_delete=models.CASCADE, editable=False)
	connections = models.ManyToManyField('authentication.User', blank=True, related_name='connections')

	def __str__(self):
		return self.user.username

	def connect(self, user):
		if not user in self.connections.all():
			self.connections.add(user)

	def remove_connection(self, user):
		if user in self.connections.all():
			self.connections.remove(user)

	def symmetrical_remove(self, user):
		self.remove_connection(user)
		target_network = get_object_or_404(Network, user=user)
		target_network.remove_connection(self.user)

	def is_connected(self, user):
		if user in self.connections.all():
			return True
		return False


class ConnectRequest(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	sender = models.ForeignKey('authentication.User', related_name='connect_requests', on_delete=models.CASCADE, editable=False)
	receiver = models.ForeignKey('authentication.User', related_name='connect_invites', on_delete=models.CASCADE, editable=False)
	is_active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.sender.username} to {self.receiver.username}'

	def accept(self):
		sender_network = get_object_or_404(Network, user=self.sender)
		sender_network.connect(self.receiver)
		receiver_network = get_object_or_404(Network, user=self.receiver)
		receiver_network.connect(self.sender)
		self.is_active = False
		self.save()

	def decline(self):
		self.is_active = False
		self.save()

	def cancel(self):
		self.is_active = False


class ConnectNotification(models.Model):
	type = models.CharField(default='connect-request', max_length=255)
	receiver = models.ForeignKey('authentication.User', related_name='notifications', on_delete=models.CASCADE, editable=False)
	is_read = models.BooleanField(default=False)
	initiated_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, editable=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.timestamp)

