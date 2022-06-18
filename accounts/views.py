from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .forms import SignupForm, ProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    update_session_auth_hash, authenticate, login, logout)
from .utils import validate_card, validate_phone, validate_exp_date
from .models import Profile


@login_required
def home_view(request):
    user = request.user
    context = {}
    if user.profile.is_client:
        return render(request, 'home-client.html', context)
    if user.profile.is_merchant:
        if not user.profile.password_changed:
            return redirect('change-password')
        else:
            return redirect('merchant-view', id=user.id)
    if user.profile.is_staff:
        return redirect('staff-view')


def register_user(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'register.html', context)


def change_password(request):
    form = ChangePasswordForm(request.user, request.POST)
    if form.is_valid():
        print(request.POST)
        user = form.save()
        update_session_auth_hash(request, user)
        profile = Profile.objects.get(user=request.user)
        profile.password_changed = True
        profile.save()
        user = authenticate(
            username=request.user.username,
            password=request.POST['new_password1'],)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
    context = {'form': form}
    return render(request, 'change_password.html', context)


def create_user_profile(request):
    form = ProfileForm(request.POST or None)
    context = {'form': form}
    user_profile = Profile.objects.get(user=request.user)
    if form.is_valid():
        query = request.POST.dict()
        if not validate_phone(query['phone']):
            context['helper'] = 'Невалиден телефонен номер'
            return render(request, 'profile.html', context)
        if not validate_card(query['card_number']):
            context['helper'] = 'Невалиден номер на карта'
            return render(request, 'profile.html', context)
        if not validate_exp_date(query['card_expires']):
            context['helper'] = 'Невалидна дата'
            return render(request, 'profile.html', context)
        user_profile.is_client = True
        user_profile.name = query['name']
        user_profile.phone = query['phone']
        user_profile.card_number = query['card_number']
        user_profile.card_expires = query['card_expires']
        user_profile.save()
        return redirect('login')

    return render(request, 'profile.html', context)


def login_user(request):
    logout(request)
    username = password = ''
    helper = None
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
        else:
            helper = "*Грешен потребител или парола"
    context = {'helper': helper}
    return render(request, 'login.html', context)
