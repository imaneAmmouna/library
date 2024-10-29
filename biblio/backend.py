from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Client

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        if email is not None:
            try:
                user = Client.objects.get(email=email)
                if user.check_password(password):  # Utiliser check_password pour vérifier le mot de passe
                    return user
                else:
                    return None
            except Client.DoesNotExist:
                return None
        else:
            return None