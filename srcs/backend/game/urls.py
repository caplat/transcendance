from django.urls import path

from .views import games, games_list, game_start, game_settings

urlpatterns = [
    path('', games, name='games'),
    path('list/<str:game_type>/', games_list, name='gameslist'),

    path('1vs1/<int:room_id>/', game_start, name='1vs1'),
    path('2vs2/<int:room_id>/', game_start, name='2vs2'),
    path('4players/<int:room_id>/', game_start, name='4players'),
    path('tournament/<int:room_id>/', game_start, name='tournament'),

    path('settings/', game_settings, name='settings'),
]
