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


class NetworkDetailView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = NetworkSerializer

	def get_object(self):
		obj = get_object_or_404(Network, id=self.kwargs['network_id'])
		return obj


class MyConnectRequestListCreateView(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ConnectRequestSerializer

	def get_queryset(self):
		queryset = ConnectRequest.objects.filter(sender=self.request.user)
		return queryset

	def post(self, request, *args, **kwargs):
		receiver = get_object_or_404(User, username=self.request.data['username'])
		request = ConnectRequest.objects.create(sender=self.request.user, receiver=receiver)
		notification = ConnectNotification.objects.create(type='connect-request', receiver=receiver, initiated_by=self.request.user)
		channel_layer = get_channel_layer()
		receiver_group = f'notifications_{receiver.username}'
		async_to_sync(channel_layer.group_send)(
			receiver_group, {
				'type': 'notify',
				'notification': json.dumps(ConnectNotificationSerializer(notification).data,cls=DjangoJSONEncoder),
			}
		)
		data = {
			'status': 'Success',
			'message': 'Request has been sent',
		}
		return JsonResponse(data)


class MyConnectInviteListAcceptDeclineView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ConnectRequestSerializer

	def get_queryset(self):
		queryset = ConnectRequest.objects.filter(receiver=self.request.user)
		return queryset

	def post(self, request, *args, **kwargs):
		sender = get_object_or_404(User, username=self.request.data['username'])
		request = ConnectRequest.objects.filter(sender=sender, receiver=self.request.user, is_active=True).first()
		type = self.request.data['type']
		if type == 'accept':
			request.accept()
			data = {
				'status': 'Success',
				'message': 'Invite has been accepted',
			}
		elif type == 'decline':
			request.decline()
			data = {
				'status': 'Success',
				'message': 'Invite has been declined',
			}
		ConnectNotification.objects.filter(receiver=self.request.user, initiated_by=sender).delete()
		return JsonResponse(data)
