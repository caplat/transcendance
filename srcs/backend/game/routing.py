from django.urls import re_path

from .onevsone_consumer import OneVsOneConsumer
from .twovstwo_consumers import TwoVsTwoConsumer
from .four_consumers import FourConsumer

websocket_urlpatterns = [
    re_path(r'ws/games/1vs1/(?P<game_type>\w+)/(?P<room_id>\w+)/$', OneVsOneConsumer.as_asgi()),
    re_path(r'ws/games/2vs2/(?P<game_type>\w+)/(?P<room_id>\w+)/$', TwoVsTwoConsumer.as_asgi()),
    re_path(r'ws/games/4players/(?P<game_type>\w+)/(?P<room_id>\w+)/$', FourConsumer.as_asgi())
]
