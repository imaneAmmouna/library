from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

# Create your models here.

######table client
class Client(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    client_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Ajoute le champ password

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return str(self.client_id)

######table auteur
class Auteur(models.Model):
    auteur_id = models.AutoField(primary_key=True)
    nom_auteur = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.nom_auteur = self.nom_auteur.upper()  # Convertir en majuscules
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom_auteur'], name='unique_auteur_name')
        ]

    def __str__(self):
        return self.nom_auteur
######table categorie
class CategorieLivre(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    nom_categorie = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom_categorie

######table livre
class Livre(models.Model):
    livre_id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.TextField(default='')  
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategorieLivre, on_delete=models.CASCADE)
    categorie = models.ManyToManyField(CategorieLivre) 
    nombre_livres = models.IntegerField(default=0)
    prix_locations = models.DecimalField(max_digits=10, decimal_places=2)
    couverture = models.ImageField(upload_to='images_cover/',blank=True)

    def __str__(self):
        return self.titre

######table location
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_location = models.DateField()
    date_retour = models.DateField(null=True, blank=True)
    prix_location = models.DecimalField(max_digits=10, decimal_places=2)

######table help
class QuestionClient(models.Model):
    question_client_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    sujet = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    reponse = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question {self.question_client_id} - Client {self.client_id.username}"

######table panier
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)

    def get_livre_id(self):
        return self.livre.livre_id

    def remove_from_cart(self):
        # Supprimer l'instance actuelle du panier
        self.delete()

    def __str__(self):
        return f"Cart for {self.client.username}"

######
######
