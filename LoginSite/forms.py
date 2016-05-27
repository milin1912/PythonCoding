from django import forms
from django.contrib.auth.models import User

from .models import Album


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['photo_title', 'upload']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']