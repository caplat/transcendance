from django.urls import path

# from .views import delete_profile, unblock_user, refuse_friend_request, block_user, remove_friends, profile, updateProfile, friends, userCreate, connexion, deconnexion, send_friend_request, accept_friend_request, uploadPassword
from . import views
urlpatterns = [
    path('register/', views.userCreate, name='register'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('friends/send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('friends/accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept_friend_request'),
    path('friends/refuse_friend_request/<int:requestID>/', views.refuse_friend_request, name='refuse_friend_request'),
    path('remove_friends/<int:userID>/', views.remove_friends, name='remove_friends'),
    path('friends/block_user/<int:userID>/', views.block_user, name='block_user'),
    path('friends/unblock_user/<int:userID>/', views.unblock_user, name='unblock_user'),
    path('profile/<username>/', views.profile, name='profile'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('pass/', views.uploadPassword, name='changePassword'),
    path('friends/', views.friends, name='friends'),
    path('delete_profile/<int:userID>/', views.delete_profile, name='delete_profile'),
]
