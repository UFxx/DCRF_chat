from django.urls import path

from .consumers import *

websocket_urlpatterns = [
    path("ws/new_user/", UserCreateConsumer.as_asgi()),
    path('ws/chat/<int:id>/', RoomConsumer.as_asgi()),
]