from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import src.apps.websocketchat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            src.apps.websocketchat.routing.websocket_urlpatterns
        )
    )
})