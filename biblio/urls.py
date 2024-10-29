from django.urls import path,include
from .views import *
from . import views

urlpatterns =[
    path('', acceuil, name="acceuil"),
    path('livre/<int:livre_id>/', livre_detail, name='livre_detail'),
    path('categorie/<int:categorie_id>/', livres_par_categorie, name='livres_par_categorie'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('createAccount/', views.createAccount_view, name='createAccount'),
    path('profile/', profile_view, name='profile'),
    path('cart/', cart_view, name='cart'),
    path('help/', help_view, name='help'),
    path('notifications/', notifications_view, name='notifications'),
    path('formLocation/', formLocation_view, name='formLocation'),
    path('add-to-cart/<int:livre_id>/', add_to_cart, name='add_to_cart'),    
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('search/', search_view, name='search'),
    path('logout/', logout_view, name='logout'),
    path('submit_location/', views.submit_location, name='submit_location'),
]