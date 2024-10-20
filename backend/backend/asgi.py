import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django.setup()
from chat.routing import websocket_urlpatterns
from chat.middleware import JwtAuthMiddlewareStack
django_asgi_app = get_asgi_application()




application = ProtocolTypeRouter({

    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": JwtAuthMiddlewareStack(

            URLRouter(websocket_urlpatterns

        )
    ),
})