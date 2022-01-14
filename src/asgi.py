import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import src.apps.chat.routing
import src.apps.networking.routing
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            src.apps.chat.routing.websocket_urlpatterns +
            src.apps.networking.routing.websocket_urlpatterns
        )
    )
})