from django.urls import path
from . import views

urlpatterns = [

    path('auth/', views.auth_42, name='auth_42'),
    path('callback/', views.callback, name='callback'),
    path('profile/', views.profile_view, name='profile'),
]