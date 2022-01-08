from rest_framework import serializers
from .models import ChatSession, Message


class MessageSerializer(serializers.ModelSerializer):
	sender = serializers.HyperlinkedRelatedField(read_only=True, view_name='user_detail')

	class Meta:
		model = Message
		fields = ('__all__')


class ChatSessionSerializer(serializers.ModelSerializer):
	initiator = serializers.HyperlinkedRelatedField(read_only=True, view_name='user_detail')
	receiver = serializers.HyperlinkedRelatedField(read_only=True, view_name='user_detail')
	session_messages = MessageSerializer(many=True, read_only=True)

	class Meta:
		model = ChatSession
		fields = ('__all__')