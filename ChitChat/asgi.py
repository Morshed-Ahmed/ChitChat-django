"""
ASGI config for ChitChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from chat.consumers import MyConsumer
from accounts.consumers import AuthConsumer
from friend.consumers import FriendRequestConsumer,UserSearchConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChitChat.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
                path("ws/chat/", MyConsumer.as_asgi()),
                path("ws/auth/", AuthConsumer.as_asgi()),
                path("ws/user-search/", UserSearchConsumer.as_asgi()),
                path("ws/friend-request/", FriendRequestConsumer.as_asgi()),
            ])
})
