from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from .models import Game, count_games_by_type

@login_required(login_url='/need_auth/')
def games(request):
    return render(request, 'game/games.html')

@login_required(login_url='/need_auth/')
def games_list(request,  game_type):
    print('GAME TYPE : ', game_type)
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        room_id = count_games_by_type(game_type) + 1
        game = Game.objects.create(game_type=game_type, room_id=room_id)
        game.save()
        response_data = {
            'redirect': True,
            'url': '/games/' + game.game_type + '/' + str(game.room_id) + '/'
        }
        return JsonResponse(response_data)

    games = Game.objects.filter(game_type=game_type)
    for game in games:
        print('GAME : ', game)
    print('END')

    context = {
        'game_type': game_type,
        'games': games
    }
    return render(request, 'game/games_list.html', context=context)

@login_required(login_url='/need_auth/')
def game_start(request, room_id):
    game_type = request.path.split('/')[2]
    print('GAME TYPE : ', game_type)

    game = Game.objects.get(game_type=game_type, room_id=room_id)
    user = request.user

    game.add_participant(user)

    print(f'USER : {user.username}, ID : {user.id}')
    print('GAME : ', game)

    context = {
        'game_type': game_type,
        'room_id': room_id,
        'user_id': user.id
    }
    return render(request, 'game/game.html', context=context)

@login_required(login_url='/need_auth/')
def game_settings(request):
    return render(request, 'game/settings.html')

