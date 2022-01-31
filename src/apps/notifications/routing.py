from django.urls import path
from .consumers import NotificationConsumer


websocket_urlpatterns = [
  path('ws/request-notification/', NotificationConsumer.as_asgi()),
]