from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User 

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')