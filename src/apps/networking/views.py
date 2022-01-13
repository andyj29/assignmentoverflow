import json
from rest_framework import permissions, generics, filters
from rest_framework import views
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from src.apps.authentication.models import User
from .serializers import NetworkSerializer, ConnectRequestSerializer, ConnectNotificationSerializer
from .models import Network, ConnectRequest, ConnectNotification


class MyNetworkDetailView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = NetworkSerializer

	def get_object(self):
		obj = get_object_or_404(Network, user=get_object_or_404(User, id=self.request.user.id))
		return obj


class MyConnectRequestListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ConnectRequestSerializer

	def get_queryset(self):
		queryset = ConnectRequest.objects.filter(sender=self.request.user)
		return queryset

	def perform_create(self, serializer):
		serializer.save(sender=self.request.user)


class MyConnectInviteListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ConnectRequestSerializer

	def get_queryset(self):
		queryset = ConnectRequest.objects.filter(receiver=self.request.user)
		return queryset


class SendRequestView(views.APIView):
	permission_class = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		receiver_username = self.kwargs['receiver_username']
		if receiver_username is not None:
			receiver = get_object_or_404(User, username=receiver_username)
			request = ConnectRequest.objects.create(sender=self.request.user, receiver=receiver)
			notification = ConnectNotification.objects.create(type='connect request', receiver=receiver, initiated_by=self.request.user)
			channel_layer = get_channel_layer()
			channel = f'notifications_{receiver.username}'
			async_to_sync(channel_layer.group_send)(
				channel, {
					'type': 'notify',
					'command': 'new_notification',
					'notification': json.dumps(ConnectNotificationSerializer(notification).data, cls=DjangoJSONEncoder),
				}
			)
			data = {
				'status': True,
				'message': 'Success',
			}
			return JsonResponse(data)


class AcceptRequestView(views.APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		sender_username = self.kwargs['sender_username']
		if sender_username is not None:
			sender = get_object_or_404(User, username=sender_username)
			request = ConnectRequest.objects.filter(sender=sender, receiver=request.user, is_active=True).first()
			request.accept()
			request.is_active = False
			request.save()
			Network
			ConnectNotification.objects.filter(receiver=request.user, initiated_by=sender).delete()
			data = {
				'status': True,
				'message': 'Success'
			}
			return JsonResponse(data)


