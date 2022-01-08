from rest_framework import generics, permissions
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, reverse
from src.apps.authentication.models import User
from .models import ChatSession
from .serializers import ChatSessionSerializer


class ChatSessionList(generics.ListCreateAPIView):
	serializer_class = ChatSessionSerializer
	permission_class = [permissions.IsAuthenticated]

	def get_queryset(self):
		return ChatSession.objects.filter(Q(initiator=self.request.user) | Q(receiver=self.request.user))

	def perform_create(self, serializer):
		username = self.request.data.pop('username')
		receiver = get_object_or_404(User, username=username)
		chat_session = ChatSession.objects.filter(Q(initiator=self.request.user, receiver=receiver) | Q(initiator=receiver, receiver=self.request.user))
		if chat_session.exists():
			return redirect(reverse('get_chat_session', args=(chat_session[0].id)))
		else:
			serializer.save(initiator=self.request.user, receiver=receiver)

		
