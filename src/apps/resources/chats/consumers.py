import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from src.apps.authentication.models import User
from .models import ChatSession, Message
from .serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.room_id = self.scope['url_route']['kwargs']['room_id']
		self.room_group_id = f'chat_{self.room_id}'

		async_to_sync(self.channel_layer.group_add)(self.room_group_id, self.channel_name)
		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(self.room_group_id, self.channel_name)

	def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		message, attachment = (
			text_data_json['message'],
			text_data_json.get('attachment'),
		)

		chat_session = ChatSession.objects.get(id=int(self.room_id))
		sender = self.scope['user']

		if attachment:
			file_str, file_ext = attachment['data'], attachment['format']
			file_data = ContentFile(base64.b64decode(file_str), name=f'{secrets.token_hex(8)}.{file_ext}')

			_message = Message.objects.create(
				sender=sender,
				attachment=file_data,
				text=message,
				chat_session=chat_session,
			)
		else:
			_message = Message.objects.create(
				sender=sender,
				text=message,
				chat_session=chat_session,
			)

		chat_type = {'type': 'chat_message'}
		message_serializer = (dict(MessageSerializer(instance=_message).data))
		return_dict = {**chat_type, **message_serializer}
		if _message.attachment:
			async_to_sync(self.channel_layer.group_send)(self.room_group_name,
				{
					'type': 'chat_message',
					'message': message,
					'sender': sender.email,
					'attachment': _message.attachment.url,
					'time': str(_message.timestamp),
				}
			)
		else:
			async_to_sync(self.channel_layer.group_send)(self.room_group_id, return_dict)

	def chat_message(self, event):
		dict_to_be_sent = even.copy()
		dict_to_be_sent.pop('type')

		self.send(text_data=json.dumps(dict_to_be_sent))