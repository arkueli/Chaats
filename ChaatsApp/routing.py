from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user-authentication/$', consumers.UserAuthConsumer.as_asgi()),
    re_path(r'ws/chat-message/$', consumers.ChatMessage.as_asgi() ),
    re_path(r'ws/user-profile/$', consumers.UserProfileConsumer.as_asgi()),
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]

