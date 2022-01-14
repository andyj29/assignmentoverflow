from django.urls import path
from .consumers import ConnectNotificationConsumer


websocket_urlpatterns = [
	path('ws/connect-request-notification/', ConnectNotificationConsumer.as_asgi()),
]