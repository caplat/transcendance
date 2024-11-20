from django.db import models
from django.contrib.auth.models import User

from user.models import User42
from matchmaking.models import Tournament, Participant


class Game(models.Model):
    game_type = models.CharField(max_length=30, verbose_name='TYPE')
    room_id = models.IntegerField(null=True, blank=True, verbose_name='ROOM_ID')
    state = models.CharField(max_length=30, default='load', verbose_name='STATE')
    participants = []
    
    def __str__(self):
        return f"game {self.game_type} {self.room_id} {self.state}"

    def add_participant(self, user):
        self.participants.append(Participant.objects.get_or_create(user=user))

    def get_participants(self):
        return self.participants


def count_games_by_type(game_type):
    game_count = Game.objects.filter(game_type=game_type).count()
    return game_count
