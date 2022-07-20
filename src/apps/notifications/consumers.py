from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

  async def connect(self):
    self.user = self.scope['user']
    self.group_layer = f'notifications_{self.user.username}'
  
    await self.channel_layer.group_add(self.group_layer, self.channel_name)
    await self.accept()

  async def disconnect(self, close_code):

    await self.channel_layer.group_discard(self.group_layer, self.channel_name)

  async def notify(self, event):
    notification = event['notification']
    await self.send_json(
      {
        'notification': notification,
      }
    )