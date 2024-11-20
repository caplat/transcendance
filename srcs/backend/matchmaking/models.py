from django.db import models
# from django.contrib.auth.models import User
from user.models import User42
from random import shuffle

class Tournament(models.Model):
    name = models.CharField(unique=True, max_length=200)
    creator = models.ForeignKey(User42, on_delete=models.CASCADE, default=1)
    is_locked = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(default=16)

    def can_lock(self):
        return 4 <= self.participants.count() <= self.max_participants
    
    def generate_matches(self):
        participants = list(self.participants.all())
        shuffle(participants)
        matches = []
        while len(participants) >=2:
            p1 = participants.pop()
            p2 = participants.pop()
            match = Match.objects.create(
                tournament=self,
                participant1=p1,
                participant2=p2
            )
            matches.append(match)

    def __str__(self):
        return self.name
    



class Participant(models.Model):
    user = models.OneToOneField(User42, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0)
    nickname = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.user.username


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.CASCADE)
    participant1 = models.ForeignKey(Participant, related_name='matches_as_participant1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(Participant, related_name='matches_as_participant2', on_delete=models.CASCADE)
    participant1_score = models.IntegerField(default=0, null=True)
    participant2_score = models.IntegerField(default=0, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.participant1} vs {self.participant2}"
