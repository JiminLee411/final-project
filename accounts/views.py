from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from django.views.decorators.http import require_POST

from .forms import CustomUserChangeForm, CustomUserCreationForm 


# Create your views here.
# def index(request):
#     context = {
#         'users' : get_user_model().objects.all()
#     }
#     return render(request, 'accounts/index.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:movies_index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def detail(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    context = {
        'user_profile' : user
    }
    return render(request, 'accounts/detail.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:movies_index')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'movies:movies_index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:movies_index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:movies_index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:movies_index')
    else:
        form = PasswordChangeForm(request.user) # 반드시 첫번째 인자로 user
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def delete(request, user_pk):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('movies:movies_index')

@login_required
def follow(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user != user:
        if user in request.user.followers.all():
            request.user.followers.remove(user)
        else:
            request.user.followers.add(user)
    return redirect('accounts:detail', user_pk)

def following(request, user_pk):
    host = get_object_or_404(get_user_model(), pk=user_pk)
    followings = host.followers.all()
    context = {
        'followings': followings,
        'host' : host,
    }
    return render(request, 'accounts/following.html', context)

def follower(request, user_pk):
    host = get_object_or_404(get_user_model(), pk=user_pk)
    followers = host.followings.all()
    context = {
        'followers': followers,
        'host' : host,
    }
    return render(request, 'accounts/follower.html', context)