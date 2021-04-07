from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from django.views import View
from movies.models import Review, Movie
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    reviews = Review.objects.filter(user=person).order_by('-created_at')

    context = {
        'person': person,
        'reviews': reviews,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, username):
    you = get_object_or_404(get_user_model(), username=username)
    me = request.user

    if me != you:
        if you. followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
        else:
            you.followers.add(me)

    return redirect('accounts:profile', you.username)

class ProfileUpdateView(View):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        user_form = CustomUserCreationForm(initial={
            'first_name': user.first_name,
            'username': user.username,
        })

        if hasattr(user, 'profile'):
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname': profile.nickname,
                'introduction': profile.introduction,
                'image': profile.image,
            })
        else:
            profile_form = ProfileForm()

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }

        return render(request, 'accounts/profile_update.html', context)

    def post(self, request, username):
        person = get_object_or_404(get_user_model(), username=username)
        user_form = CustomUserCreationForm(request.POST, instance=person)

        if user_form.is_valid():
            user_form.save()

        if hasattr(person, 'profile'):
            profile = person.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = person
            profile.save()

        return redirect('accounts:profile', person.username)
        
def followerswings(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    
    context = {
        'person': person,
    }

    return render(request, 'accounts/followerswings.html', context)

class AccountUpdateView(View):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        user_form = CustomUserCreationForm(initial={
            'first_name': user.first_name,
            'username': user.username,
        })

        context = {
            "user_form": user_form,
        }

        return render(request, 'accounts/account_update.html', context)

    def post(self, request, username):
        person = get_object_or_404(get_user_model(), username=username)
        user_form = CustomUserCreationForm(request.POST, instance=person)

        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, person)

        return redirect('accounts:profile', person.username)