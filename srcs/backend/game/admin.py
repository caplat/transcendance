from django.contrib import admin

from .models import Game

@admin.register(Game)
class AdminUsers(admin.ModelAdmin):
    list_display = ('id', 'game_type', 'room_id', 'state', 'participants')
 