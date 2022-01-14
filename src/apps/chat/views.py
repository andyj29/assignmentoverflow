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

	def post(self, request, *args, **kwargs):
		receiver = get_object_or_404(User, username=self.request.data['username'])
		chat_sessions = ChatSession.objects.filter(Q(initiator=self.request.user, receiver=receiver) | Q(initiator=receiver, receiver=self.request.user))
		chat_session = chat_sessions.first()
		if chat_session is None:
			serializer = ChatSessionSerializer(data=self.request.data)
			if serializer.is_valid():
				chat_session = serializer.save(initiator=self.request.user, receiver=receiver)
		return redirect('v1:chat:chat_session_detail', session_id=chat_session.id)


class ChatSessionDetailView(generics.RetrieveAPIView):
	serializer_class = ChatSessionSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		chat_session = get_object_or_404(ChatSession, pk=self.kwargs['session_id'])
		return chat_session