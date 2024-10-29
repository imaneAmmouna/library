
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Livre, CategorieLivre, Client, QuestionClient, Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth, messages
from .forms import ClientForm, LoginForm, LocationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse


# Create your views here.

#####acceuil view
def acceuil(request):
    # Récupérer les 10 premiers livres de chaque catégorie
    categories = CategorieLivre.objects.all()
    livres_par_categorie = {}
    for categorie in categories:
        livres = Livre.objects.filter(categorie=categorie)[:10]
        livres_par_categorie[categorie] = livres
    return render(request, 'acceuil.html', {'livres_par_categorie': livres_par_categorie})

#####detail de chaque livre
def livre_detail(request, livre_id):
    # Récupérer le livre à afficher en fonction de son ID
    livre = get_object_or_404(Livre, pk=livre_id)
    return render(request, 'livre_detail.html', {'livre': livre})

#####les livres par leurs categories
def livres_par_categorie(request, categorie_id):
    categorie = get_object_or_404(CategorieLivre, pk=categorie_id)
    livres = Livre.objects.filter(categorie=categorie)
    return render(request, 'livres_par_categorie.html', {'categorie': categorie, 'livres': livres})

#####create account
def createAccount_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print("email:",email)
            print("pass1 :",password)
            client.password = make_password(password)
            print("make pass :",client.password)
            print("*******************")
            client.save()
            messages.success(request, "Your account has been created successfully.")
            return redirect('login')
        else:
            messages.error(request, "An error has occurred. Please correct the errors and try again.")
    else:
        form = ClientForm()
    return render(request, 'createAccount.html', {'form': form})

#####se connecter
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Client.objects.get(email=email)
            if user.check_password(password):
                # Authentification réussie, rediriger vers la page d'accueil ou toute autre page appropriée
                # Vous pouvez également utiliser la fonctionnalité de session de Django pour stocker l'utilisateur connecté
                request.session['client_id'] = user.client_id
                return redirect('home')
            else:
                # Mot de passe incorrect
                messages.error(request, 'Invalid email or password.')
        except Client.DoesNotExist:
            # Utilisateur non trouvé
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')        

#####la page home de chaque client
def home_view(request):
    categories = CategorieLivre.objects.all()
    livres_par_categorie = {}
    for categorie in categories:
        livres = Livre.objects.filter(categorie=categorie)[:10]
        livres_par_categorie[categorie] = livres
    return render(request, 'home.html', {'livres_par_categorie': livres_par_categorie})

#####la page profile de chaque client
def profile_view(request):
    # Récupérer l'identifiant du client à partir de la session
    client_id = request.session.get('client_id')
    if client_id:
        # Récupérer les informations du client à partir de l'identifiant
        client = Client.objects.get(client_id=client_id)
        return render(request, 'profile.html', {'client': client})
    # Si aucun identifiant client n'est trouvé dans la session, afficher la page de profil sans données
    return render(request, 'profile.html')

#####la page du panier "cart" affichage du contenu du panier
def cart_view(request):
    # Récupérer l'ID du client à partir de la session
    client_id = request.session.get('client_id')        
    print("client_id",client_id)

    # Récupérer le client à partir de l'ID
    client = get_object_or_404(Client, client_id=client_id)
    # Récupérer tous les livres dans le panier de l'utilisateur
    livres_du_panier = Cart.objects.filter(client=client)
    context = {
        'livres_du_panier': livres_du_panier
    }
    return render(request, 'cart.html', context)

#####stockés le livre lorsque le client clique sur add to cart
def add_to_cart(request, livre_id):
    if request.method == 'POST':
        # Récupérer l'ID du client à partir de la session
        client_id = request.session.get('client_id')
        
        # Vérifier si l'ID du client existe dans la session
        if client_id is None:
            return JsonResponse({'error': 'Client non authentifié'}, status=401)
        
        # Ajouter le livre au panier du client avec ses informations
        Cart.objects.create(client_id=client_id, livre_id=livre_id)

        return JsonResponse({'message': 'Livre ajouté au panier avec succès'}, status=200)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

##### supprimer un livre du panier
def remove_from_cart(request, cart_id):
    if request.method == 'POST':
        # Récupérer l'instance du panier à supprimer
        cart = get_object_or_404(Cart, pk=cart_id)
        # Supprimer le panier
        cart.delete()
        # Renvoyer une réponse JSON pour indiquer que la suppression a réussi
        return redirect('cart')    # Si la méthode de la requête n'est pas POST, renvoyer une réponse JSON d'erreur
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

#####la page d'aide
def help_view(request):
    client_id = request.session.get('client_id')    
    if request.method == 'POST':
        # Si la méthode de la requête est POST, cela signifie que le formulaire a été soumis
        sujet = request.POST.get('subject')
        description = request.POST.get('description')
        
        if client_id:
            client = Client.objects.get(client_id=client_id)
            # Créer une nouvelle instance de QuestionClient avec les données soumises
            question_client = QuestionClient.objects.create(
                client_id=client,
                sujet=sujet,
                description=description
            )
            # Rediriger l'utilisateur vers une page de confirmation
            confirmation_message = "Votre message a été envoyé avec succès ! Attendre une réponse."
            return render(request, 'help.html', {'confirmation_message': confirmation_message})
        else:
            # Gérer le cas où l'identifiant du client n'est pas présent dans la session
            return render(request, 'error_page.html', {'error_message': 'Client ID not found in session.'})
    else:
        # Si la méthode de la requête n'est pas POST, cela signifie que l'utilisateur accède simplement à la page d'aide
        client_id = request.session.get('client_id')
        if client_id:
            # Récupérer les informations du client à partir de l'identifiant
            client = Client.objects.get(client_id=client_id)
            return render(request, 'help.html', {'client': client})
        return render(request, 'help.html')

#####les notifications
def notifications_view(request):
     # Récupérer toutes les questions avec leurs réponses associées
    questions_with_responses = QuestionClient.objects.exclude(reponse__isnull=True).exclude(reponse__exact='')

    # Passer les données au modèle HTML
    return render(request, 'notifications.html', {'questions_with_responses': questions_with_responses})

##### remplir le formulaire de location
def formLocation_view(request):
    livre_id = request.GET.get('livre_id')
    client_id = request.session.get('client_id')  # Récupérer l'ID du client depuis la session

    if client_id:
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            return HttpResponse("Client not found", status=404)
    else:
        return HttpResponse("Client ID not found in session", status=404)

    try:
        livre = Livre.objects.get(pk=livre_id)
    except Livre.DoesNotExist:
        return HttpResponse("Book not found", status=404)

    return render(request, 'formLocation.html', {'livre': livre, 'client': client})

##### passer les donnees du formulaire à la BD
def submit_location(request):
    if request.method == 'POST':
        print("Method is POST")
        form = LocationForm(request.POST)
        print(form.errors)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        print("Method is not POST")
        form = LocationForm()

    return render(request, 'formLocation.html', {'form': form})

##### search bar
def search_view(request):
    query = request.GET.get('query')
    if query:
        # Recherchez les livres correspondant à la requête
        livres = Livre.objects.filter(titre__icontains=query)
    else:
        livres = Livre.objects.none()  # Aucune recherche effectuée si la requête est vide
    return render(request, 'search_results.html', {'livres': livres, 'query': query})

#####se deconnecter
def logout_view(request):
    logout(request)
    return redirect('acceuil') 