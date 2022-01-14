import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core import serializers

from .models import ConnectNotification
from .serializers import ConnectNotificationSerializer


class ConnectNotificationConsumer(AsyncJsonWebsocketConsumer):

	@database_sync_to_async
	def fetch_notifications(self):
		user = self.scope['user']
		notifications = ConnectNotification.objects.filter(receiver=user, type='connect request').select_related('initiated_by')
		serializer = ConnectNotificationSerializer(notifications, many=True)
		content = {
			'command': 'notifications',
			'notifications': json.dumps(serializer.data)
		}

		self.send_json(content)

	def notifications_to_json(self, notifications):
		output = []
		for notification in notifications:
			output.append(self.notification_to_json(notification))
		return output

	@staticmethod
	def notification_to_json(notification):
		return {
			'initiated_by': serializers.serialize('json', [notification.initiated_by]),
			'receiver': serializers.serialize('json', [notification.receiver]),
			'timestamp': str(notification.timestamp)
		}

	async def connect(self):
		user = self.scope['user']
		group_layer = f'notifications_{user.username}'
		await self.accept()
		await self.channel_layer.group_add(group_layer, self.channel_name)

	async def disconnect(self, close_code):
		user = self.scope['user']
		group_layer = f'notifications_{user.username}'
		await self.channel_layer.group_discard(group_layer, self.channel_name)

	async def notify(self, event):
		await self.send_json(event)

	async def receive(self, text_data=None, bytes_data=None, **kwargs):
		data = json.loads(text_data)
		if data['command'] == 'fetch_connect_notifications':
			await self.fetch_notifications()