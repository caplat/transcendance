from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.urls import path
# import os
# from backend.settings import BASE_DIR


# tentative changer langue
# def load_files(request, langue):
#     file = open(os.path.join(BASE_DIR, 'static/js', langue ), 'rb')
#     response = HttpResponse(langue, content_type='application/javascript')


def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )

    def login_view(request):
        if request.user.is_authenticated:
            return redirect('/home/')
    if function:
        return actual_decorator(function)
    return actual_decorator


@logout_required(logout_url='/home/')
def index(request):
    return render(request, "index.html")

@login_required(login_url='/need_auth/')
def home(request):
    return render(request, 'home.html')

def need_auth(request):
    return render(request, 'need_auth.html')


# pages errors
def page404(request, exception):
    return render(request,'page404.html')

def page400(request, exception):
    return render(request,'page400.html')

def page403(request, exception):
    return render(request,'page403.html')

def page500(request):
    return render(request,'page500.html')
