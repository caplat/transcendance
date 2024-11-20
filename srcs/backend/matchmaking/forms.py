from django import forms
from .models import Match, Tournament, Participant
# from django.contrib.auth.models import User


class MatchForm(forms.ModelForm):
    participant1 = forms.ModelChoiceField(
        queryset=Participant.objects.all(),
        label='Participant 1',
        required=True
    )
    participant2 = forms.ModelChoiceField(
        queryset=Participant.objects.all(),
        label='Participant 2',
        required=True
    )

    class Meta:
        model = Match
        fields = ['participant1', 'participant2',]


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name',]
