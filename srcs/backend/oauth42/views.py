from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserProfile

CLIENT_ID = 'u-s4t2ud-32ba26dd6d00acc8eab465eebd38107f045ce385f15f748d826983257ccad5a6'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://10.13.4.2:8000/oauth42/callback/'

def auth_42(request):
     # Rediriger l'utilisateur vers la page d'autorisation
    auth_url = (f"https://api.intra.42.fr/oauth/authorize?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code")
    return redirect(auth_url)

def callback(request):
    # Récupérer le code d'autorisation de la requête
    code = request.GET.get('code')
    if not code:
        return render(request, 'oauth42/error.html', {'message': 'Authorization code not found.'})
    
    # Échanger le code contre un jeton d'accès
    token_url = "https://api.intra.42.fr/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    if token_response.status_code != 200:
        return render(request, 'error.html', {'message': 'Failed to obtain access token.'})

    token_json = token_response.json()
    access_token = token_json.get('access_token')

    # Utiliser le jeton d'accès pour obtenir les données de l'utilisateur
    user_info_response = requests.get(
        'https://api.intra.42.fr/v2/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    user_info = user_info_response.json()
    profile_picture_medium = user_info.get('image', {}).get('versions', {}).get('medium', '')

    # print(user_info)

    user, created = User.objects.get_or_create(
        username=user_info.get('login'),
        defaults={
            'email': user_info.get('email', ''),
            'first_name': user_info.get('first_name', ''),
            'last_name': user_info.get('last_name', ''),
        }
    )

    # Mettre à jour ou créer le profil utilisateur
    UserProfile.objects.update_or_create(
        user=user,
        defaults={
            'username': user_info.get('login'),
            'id_42': user_info.get('id'),
            'email': user_info.get('email', ''),
            'first_name': user_info.get('first_name', ''),
            'last_name': user_info.get('last_name', ''),
            'profile_picture': profile_picture_medium,
        }
    )


    # Connecter l'utilisateur et rediriger vers la page de profil
    login(request, user)
    return redirect('profile')

def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    # print("\n\ntest\n\n", user_profile.profile_picture, "\n\n")
    return render(request, 'oauth42/profile.html', {'user_profile': user_profile})




