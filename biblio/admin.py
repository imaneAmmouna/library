from django.contrib import admin
from .models import Livre, Auteur, CategorieLivre, Client, Location, QuestionClient, Cart

admin.site.register(Livre)
admin.site.register(Auteur)
admin.site.register(CategorieLivre)
admin.site.register(Client)
admin.site.register(Location)
admin.site.register(QuestionClient)
admin.site.register(Cart)