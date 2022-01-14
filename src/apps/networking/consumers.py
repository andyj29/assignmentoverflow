from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ConnectNotificationConsumer(AsyncJsonWebsocketConsumer):

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
		notification = event['notification']
		await self.send_json(
			{
				'notification': notification,
			}
		)

	