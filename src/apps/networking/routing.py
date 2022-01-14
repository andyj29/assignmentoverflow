from django.urls import path
from .consumers import ConnectNotificationConsumer


websocket_urlpatterns = [
	path('ws/connectrequestnotification/', ConnectNotificationConsumer.as_asgi()),
]