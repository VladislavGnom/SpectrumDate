from django.urls import re_path
from core import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/online-status/$', consumers.OnlineStatusConsumer.as_asgi()),
]
