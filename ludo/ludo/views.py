from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise


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
    list_mise = Mise.objects.filter(etat_validation=True, etat_suppression=False)
    return render(request, 'index.html', locals())






