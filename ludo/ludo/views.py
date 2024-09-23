from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise
from ludo.enum import Visibilite
from player.models import Partie


def custom_login_redirect(request):
    
    # Récupérer l'utilisateur connecté
    user = request.user
    # Si l'utilisateur est authentifié via Facebook
    if user.is_authenticated:
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            social_account = SocialAccount.objects.get(user=user, provider='facebook')

            # Afficher les informations du compte social
            print(social_account.extra_data)
        except SocialAccount.DoesNotExist:
            print("L'utilisateur n'a pas de compte social lié à Facebook")

    # dd(request)
    print("ici")
    # Si l'utilisateur essaie d'accéder à la page de connexion normale, on le redirige vers Facebook
    return redirect('/accounts/facebook/login/')


def index(request):
    liste_mises = Mise.objects.filter(etat_validation=True, etat_suppression=False)
    # parcourons les mises pour creer des parties ou recuperons celles en attentes
    for mise in liste_mises:
        for nb_participants in range(mise.nombre_minimum,5):
            if nb_participants >= 2 and nb_participants <= 4:
                partie = Partie.objects.filter(nombre_participants=nb_participants,
                                               montant_mise = mise.montant, 
                                               visibilite = Visibilite.Public, 
                                               etat_validation=True, etat_suppression=False)
    return render(request, 'index.html', locals())






