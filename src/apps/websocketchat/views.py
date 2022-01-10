from rest_framework import generics, permissions
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from src.apps.authentication.models import User
from .models import ChatSession
from .serializers import ChatSessionSerializer


class ChatSessionListView(generics.ListCreateAPIView):
	serializer_class = ChatSessionSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return ChatSession.objects.filter(Q(initiator=self.request.user) | Q(receiver=self.request.user))

	def perform_create(self, serializer):
		receiver_username = self.request.data['username']
		receiver = get_object_or_404(User, username=receiver_username)
		chat_session = ChatSession.objects.filter(Q(initiator=self.request.user, receiver=receiver) | Q(initiator=receiver, receiver=self.request.user))
		if chat_session.exists():
			return redirect('v1:chat:chat_session_detail', session_id=chat_session[0].pk)
		else:
			serializer.save(initiator=self.request.user, receiver=receiver)


class ChatSessionDetailView(generics.RetrieveAPIView):
	serializer_class = ChatSessionSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		chat_session = get_object_or_404(ChatSession, pk=self.kwargs['session_id'])
		return chat_session