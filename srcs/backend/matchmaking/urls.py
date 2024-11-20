from django.urls import path
from . import views

urlpatterns = [
    path('', views.tournament, name='tournament'),
    path('tournament/', views.tournament_list, name='tournament_list'),
    path('tournament/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('tournament/create/', views.tournament_create, name='tournament_create'),
    # path('tournament/<int:tournament_id>/match/create/', views.match_create, name='match_create'),
    # path('tournament/<int:tournament_id>/inscription/', views.inscription, name='inscription]'),
]
