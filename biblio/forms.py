from django import forms
from .models import Client, Location

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'nom', 'prenom', 'date_de_naissance', 'genre', 'email', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['client', 'livre', 'date_location', 'date_retour', 'prix_location']