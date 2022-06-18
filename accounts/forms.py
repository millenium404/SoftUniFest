from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        labels = {
            'name': 'Име и Фамилия',
            'phone': 'Телефонен номер',
            'card_number': 'Номер на дебитна карта',
            'card_expires': 'Валидност на картата (MM/YY)',
        }

        fields = [
            'name',
            'phone',
            'card_number',
            'card_expires',
            ]
