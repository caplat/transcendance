from django.contrib import admin
from .models import Tournament, Participant, Match

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament']

