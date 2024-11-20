from django.shortcuts import render, get_object_or_404, redirect
from .models import Tournament, Participant, Match
from .forms import MatchForm, TournamentForm
from django.contrib.auth.models import User
from user.models import User42
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='/need_auth/')
def tournament(request):
    return render(request, 'matchmaking/tournament.html')


@login_required(login_url='/need_auth/')
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'matchmaking/tournament_list.html',{'tournaments': tournaments})


# @login_required(login_url='/need_auth/')
# def tournament_detail(request, tournament_id):
#     tournament = get_object_or_404(Tournament, pk=tournament_id)
#     participants = tournament.participants.all()
#     matches = tournament.matches.all()
#     return render(request, 'matchmaking/tournament_detail.html',{
#         'tournament': tournament,
#         'participants': participants,
#         'matches': matches
#     })

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Tournament, Participant
from django.contrib.auth.decorators import login_required

@login_required(login_url='/need_auth')
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    participants = tournament.participants.all()
    matches = tournament.matches.all()
    is_user_registered = participants.filter(user=request.user).exists()
    is_creator = tournament.creator == request.user

    # Traitement des requêtes AJAX
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Inscription
        if 'subscribe' in request.POST:
            if tournament.is_locked:
                return JsonResponse({'error': "Le tournoi est verrouillé. Les inscriptions sont fermées."}, status=400)

            if tournament.participants.count() >= tournament.max_participants:
                return JsonResponse({'error': "Le nombre maximum de participants a été atteint."}, status=400)
            
            nickname = request.POST.get('nickname', '').strip()
            if not nickname:
                return JsonResponse({'error': "Le pseudo est obligatoire pour s'inscrire"}, status=400)

            participant, created = Participant.objects.get_or_create(user=request.user, tournament=tournament)

            if created:
                if Participant.objects.filter(nickname=nickname, tournament=tournament).exists():
                    participant.delete()
                    return JsonResponse({'error': "Ce pseudo est déjà utilisé dans ce tournoi."}, status=400)

                participant.nickname = nickname
                participant.save()
                return JsonResponse({
                    'message': f"Vous êtes maintenant inscrit au tournoi avec le pseudo '{nickname}'!",
                    'redirect': True,
                    'url': f'/matchmaking/tournament/{tournament_id}'
                })
            else:
                return JsonResponse({'info': "Vous êtes déjà inscrit à ce tournoi.", 'redirect': False})

        # Désinscription
        elif 'unsubscribe' in request.POST:
            participant = tournament.participants.filter(user=request.user).first()
            if participant:
                participant.delete()
                return JsonResponse({
                    'message': 'Vous vous êtes désinscrit du tournoi.',
                    'redirect': True,
                    'url': f'/matchmaking/tournament/{tournament_id}'
                })
            else:
                return JsonResponse({'error': 'Vous n’êtes pas inscrit à ce tournoi.'}, status=400)

        # Suppression du tournoi
        elif 'delete_tournament' in request.POST:
            if is_creator:
                tournament.delete()
                return JsonResponse({
                    'message': 'Le tournoi a été supprimé avec succès.',
                    'redirect': True,
                    'url': '/matchmaking/tournament/'
                })
            else:
                return JsonResponse({'error': "Vous n'avez pas la permission de supprimer ce tournoi."}, status=403)

        # Verrouillage du tournoi
        elif 'lock_tournament' in request.POST:
            if is_creator:
                if tournament.can_lock():
                    tournament.is_locked = True
                    tournament.save()
                    tournament.generate_matches()
                    return JsonResponse({'message': 'Le tournoi a été verrouillé avec succès.', 'redirect': False})
                else:
                    return JsonResponse({
                        'error': "Le tournoi doit avoir entre 4 et 16 participants pour être verrouillé."
                    }, status=400)
            else:
                return JsonResponse({'error': "Vous n'avez pas la permission de verrouiller ce tournoi."}, status=403)

        else:
            return JsonResponse({'error': "Action POST non reconnue."}, status=400)

    # Requête GET classique pour afficher la page
    return render(request, 'matchmaking/tournament_detail.html', {
        'tournament': tournament,
        'participants': participants,
        'matches': matches,
        'is_user_registered': is_user_registered,
        'is_creator': is_creator,
    })

        # return redirect('tournament_detail', tournament_id=tournament.id)
        # response_data = {
        #     'redirect': True,
        #     'url': '/matchmaking/tournament/' + str(tournament.id)
        # }
        # return JsonResponse(response_data)



@login_required(login_url='/need_auth/')
def tournament_create(request):
    form = TournamentForm()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = TournamentForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New tournament is created")
            response_data = {
                'redirect': True,
                'url': '/matchmaking/tournament/'
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Try again'})
            # return redirect('tournament_list')
    # else:
    #     form = TournamentForm()
    return render(request, 'matchmaking/tournament_create.html', {'form': form})

# @login_required(login_url='/need_auth/')
# def match_create(request, tournament_id):
#     tournament = get_object_or_404(Tournament, pk=tournament_id)

#     if request.method == 'POST':
#         form = MatchForm(request.POST)
#         if form.is_valid():
#             # Récupère les participants en fonction des utilisateurs sélectionnés
#             participant1 = form.cleaned_data['participant1']
#             participant2 = form.cleaned_data['participant2']

#             # Crée le match avec les participants sélectionnés
#             match = form.save(commit=False)
#             match.tournament = tournament
#             match.save()

#             return redirect('tournament_detail', tournament_id=tournament.id)
#     else:
#         form = MatchForm()

#     return render(request, 'matchmaking/match_create.html', {'form': form, 'tournament': tournament})

# @login_required(login_url='/need_auth/')
# def inscription(request, tournament_id):
#     tournament = get_object_or_404(Tournament, id=tournament_id)
#     if request.method == 'POST':
#         selected_users = request.POST.getlist('users')  # Récupère les utilisateurs sélectionnés
#         for user_id in selected_users:
#             user = User42.objects.get(id=user_id)
#             Participant.objects.get_or_create(user=user, tournament=tournament)
#         return redirect('tournament_detail', tournament_id=tournament.id)
#     else:
#         users = User42.objects.all()
#         return render(request, 'matchmaking/inscription.html', {'tournament': tournament, 'users': users})
