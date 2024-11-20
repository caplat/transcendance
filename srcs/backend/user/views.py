from django.shortcuts import render, redirect
from .models import User42, Friend_request
from .form import UserForm, UserUpdateForm, ChangePasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from backend.views import logout_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required(login_url='/need_auth/')
def profile(request, username):
    name = User42.objects.get(username=username)
    return render(request, 'profile.html', {'name':name})


@login_required(login_url='/need_auth/')
def updateProfile(request):
    user = request.user
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update load')
            response_data = {
                'redirect': True,
                'url': '/user/profile/' + user.username
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'error update profile'})
    else:
        form = UserUpdateForm(instance=user)
    form_errors = form.errors.as_data()
    return render(request, 'updateProfile.html', {'form': form,'form_errors': form_errors,})


@login_required(login_url='/need_auth/')
def uploadPassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if form.is_valid():
            form.save()
            messages.success(request, "Your password updated")
            update_session_auth_hash(request, form.user)
            response_data = {
                'redirect': True,
                'url': '/user/profile/' + request.user.username
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'error update password'})
    return render(request, 'changePassword.html', {'form': form})


@logout_required(logout_url='/home/')
def userCreate(request):
    form = UserForm()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = UserForm(data=request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "You are register")
            response_data = {
                'redirect': True,
                'url': '/user/login/'
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Try again'})
            # messages.error(request, form.errors)
    return render(request, 'register.html', {'form': form})


@logout_required(logout_url='/home/')
def connexion(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            user.is_connected = True
            user.status = "online"
            user.save()
            # lang = request.user.language
            # print(lang)
            # brython.js("currentLang=lang")
            messages.success(request, 'Welcome' + " " + user.username)
            response_data = {
                'redirect': True,
                'url': '/home/'
            }
            response = user.set_id_cookie(JsonResponse(response_data))

            return response
        else:
            return JsonResponse({'error': 'Error authentification'})
    # print("co test")
    return render(request, 'login.html')


@login_required(login_url='/need_auth/')
def deconnexion(request):
    user = request.user
    user.is_connected = False
    user.status = "offline"
    user.save()
    logout(request)
    return redirect('index')


@login_required(login_url='/need_auth/')
def delete_profile(request, userID):
    user = User42.objects.get(id=userID)
    user.delete()
    messages.success(request, "Profile deleted")
    # return redirect('index')
    return render(request, 'index.html')


@login_required(login_url='/need_auth/')
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User42.objects.get(id=userID)
    if to_user.id != from_user.id:
        friend_request, created = Friend_request.objects.get_or_create(
            from_user=from_user, to_user=to_user)
        if created:
            messages.success(request, 'friend request sent')
            return redirect('friends')
        else:
            messages.error(request, 'friend request was already sent')
            return redirect('friends')
    else:
        messages.error(request, "You can't invite yourself!")
        return redirect('friends')


@login_required(login_url='/need_auth/')
def accept_friend_request(request, requestID):
    friend_request = Friend_request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.success(request, 'friend request accepted')
        return redirect('friends')
    else:
        messages.error(request, 'friend request deleted')
        return redirect('friends')


@login_required(login_url='/need_auth/')
def refuse_friend_request(request, requestID):
    friend_request = Friend_request.objects.get(id=requestID)
    friend_request.delete()
    messages.success(request, 'friend request deleted')
    return redirect('friends')


@login_required(login_url='/need_auth/')
def remove_friends(request, userID):
    user = request.user
    friends = user.friends
    friends.remove(userID)
    otheruser = User42.objects.get(id=userID)
    otheruser.friends.remove(user.id) 
    return redirect('friends')


@login_required(login_url='/need_auth/')
def block_user(request, userID):
    from_user = request.user
    to_user = User42.objects.get(id=userID)
    if to_user.friends.filter(id=from_user.id).exists():
        # print("friend list:")
        # print(from_user.friends.all())
        # print(to_user.friends.all())
        from_user.friends.remove(to_user.id)
        to_user.friends.remove(from_user.id)
    #     print("friend list2:")
    #     print(from_user.friends.all())
    #     print(to_user.friends.all())
    from_user.blackList.add(to_user)
    # list = from_user.blackList.all()
    # list2 = to_user.blackList.all()
    # print("list:")
    # print(list)
    # print("")
    # # print(to_user)
    # print("list2:")
    # print(list2)
    return redirect('friends')

@login_required(login_url='/need_auth/')
def unblock_user(request, userID):
    from_user = request.user
    to_user = User42.objects.get(id=userID)
    # print(from_user.username)
    # print(to_user.username)
    if from_user.blackList.filter(id=to_user.id).exists():
        #  print("blacklist")
        from_user.blackList.remove(to_user)

    # list = from_user.blackList.all()
    # list2= to_user.blackList.all()
    # print("list:")
    # print(list)
    # print("")
    # # print(to_user)
    # print("list2:")
    # print(list2)
    # print(from_user.blackList.all())
    return redirect('friends')




# def getLanguage(request):
#     lang = request.user.language
#     print(lang)
    # return JsonResponse(lang)


@login_required(login_url='/need_auth/')
def friends(request):
    users = User42.objects.all()
    friend_requests = Friend_request.objects.all()
    return render(request, 'friends.html', {'users': users, 'friend_requests': friend_requests},)
