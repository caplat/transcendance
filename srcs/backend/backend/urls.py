"""
URL configuration for PongGame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import handler404, handler403, handler500, handler400
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from user import views
# from matchmaking import views
from backend.views import need_auth, home, index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.connexion, name='login'),
    path('oauth42/', include('oauth42.urls')),
    # path('matchmaking/', include('matchmaking.urls')),
    path('home/', home, name='home'),
    path('user/', include("user.urls")),
    path('need_auth/', need_auth, name='need_auth'),
    # path('login42/', connexion42, name='login42'),
    path('games/', include("game.urls")),
    path('matchmaking/', include("matchmaking.urls")),
    path('chat/', include('chat.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT)

handler404="backend.views.page404"
handler403="backend.views.page403"
handler500="backend.views.page500"
handler400="backend.views.page400"
