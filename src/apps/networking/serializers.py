from rest_framework import serializers
from .models import Network, ConnectRequest, ConnectNotification


class NetworkSerializer(serializers.ModelSerializer):
	user = serializers.HyperlinkedIdentityField(view_name='v1:auth:user_detail', lookup_url_kwarg='user_id')
	class Meta:
		model = Network
		fields = ('__all__')


class ConnectRequestSerializer(serializers.ModelSerializer):
	sender = serializers.HyperlinkedRelatedField(view_name='v1:auth:user_detail', read_only=True, lookup_url_kwarg='user_id')
	receiver = serializers.HyperlinkedRelatedField(view_name='v1:auth:user_detail', read_only=True, lookup_url_kwarg='user_id')
	class Meta:
		model = ConnectRequest
		fields = ('__all__')


class ConnectNotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = ConnectNotification
		fields = ('__all__')