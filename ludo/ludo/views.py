from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise
from ludo.enum import Visibilite
from ludo.utils import CurrentConfig, CurrentTauxCommission, DetermineCagnotte, DetermineCommission
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
    
    # determinons l'ensemble des mises possibles
    liste_mises = Mise.objects.filter(etat_validation=True, etat_suppression=False)
    
    # parcourons les mises pour creer des parties ou recuperons celles en attentes en fonction
    for mise in liste_mises:
        for nombre_participants in range(mise.nombre_minimum,5):
            if nombre_participants >= 2 and nombre_participants <= 4:
                partie = Partie.objects.filter(nombre_participants=nombre_participants,
                                               montant_mise = mise.montant, 
                                               visibilite = Visibilite.Public, 
                                               etat_demarrage = False,
                                               etat_validation=True, etat_suppression=False).first()
                if partie:
                    # partie deja existante donc en ligne
                    pass
                else:
                    partie = Partie()
                    partie.config = CurrentConfig()
                    partie.delai_tour = CurrentConfig().delai_tour if CurrentConfig() and CurrentConfig().delai_tour else None
                    partie.mise = mise
                    partie.montant_mise = mise.montant
                    partie.nombre_participants = nombre_participants
                    partie.montant_cagnotte = DetermineCagnotte(mise.montant, nombre_participants, CurrentTauxCommission().taux if CurrentTauxCommission() and CurrentTauxCommission().taux else None)
                    partie.montant_commission = DetermineCommission(mise.montant, nombre_participants, CurrentTauxCommission().taux if CurrentTauxCommission() and CurrentTauxCommission().taux else None)
                    partie.taux_comission = CurrentTauxCommission()
                    partie.save()
    
    # recuperons les parties valides pretes a recevoir des joueurs
    liste_parties = Partie.objects.filter(visibilite = Visibilite.Public, etat_demarrage = False, etat_validation=True, etat_suppression=False)

    # partie privee pour utilisateur connecté


    return render(request, 'index.html', locals())






