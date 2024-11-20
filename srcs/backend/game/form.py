from django import forms

from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'type',
            'room_id',
            'state'
        ]

    def __init__(self, game_type=None, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

        if game_type:
            self.fields['type'].initial = game_type
    
        self.fields['state'].initial = 'load' 
