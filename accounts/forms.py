from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Photo, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name']

class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction', 'image']