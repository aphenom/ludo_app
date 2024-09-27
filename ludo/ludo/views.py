from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise
from ludo.enum import Visibilite
from ludo.utils import CurrentConfig, CurrentTauxCommission, DetermineCagnotte, DetermineCommission
from player.models import Participation, Partie, Profil
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_dump_die.middleware import dd
from urllib.parse import urlencode


def facebook_login_with_state(request):
    # Ajouter des paramètres que tu souhaites passer dans l'URL de redirection
    next_url = request.GET.get('next', '/')
    custom_variable = 'custom_value'  # Variable que tu veux passer
    custom_variable = request.GET.get('custom_variable', custom_variable)
    state = urlencode({'next': next_url, 'custom_variable': custom_variable})
    
    # Rediriger vers l'URL de login de Facebook avec le paramètre `state`
    facebook_login_url = f'/accounts/facebook/login/?{state}'
    return redirect(facebook_login_url)


def custom_login_redirect(request):
    # Récupérer les paramètres de `state` dans la requête
    next_url = request.GET.get('next', '/')
    custom_variable = request.GET.get('custom_variable', '')

    # Exemple d'utilisation : récupérer l'utilisateur connecté via Facebook
    if request.user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='facebook')
            # Tu peux accéder aux données du profil Facebook de l'utilisateur ici
            facebook_data = social_account.extra_data
            name = facebook_data.get('name')
            email = facebook_data.get('email')
            # Ajoute ici tes traitements en fonction de `custom_variable` ou des données utilisateur
        except SocialAccount.DoesNotExist:
            return HttpResponse("Erreur: aucun compte Facebook trouvé.", status=404)

    # Rediriger vers la page souhaitée avec les informations supplémentaires
    return redirect(next_url)


#@login_required
def index(request):
    
    dd(request)
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
    # Récupérer l'utilisateur connecté
    user = request.user
    # Si l'utilisateur est authentifié via Facebook
    if user.is_authenticated:
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=user)

            partie_privee = Partie.objects.filter(organise_par=profil, visibilite = Visibilite.Privee, etat_demarrage = False, etat_validation=True, etat_suppression=False).first()

            participation_en_cours = Participation.objects.filter(partie__etat_fin = False, partie__etat_validation=True, partie__etat_suppression=False, etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False).first()
            
            if participation_en_cours:
                partie_en_cours = participation_en_cours.partie
            # Afficher les informations du compte social
            print(profil)
        except Profil.DoesNotExist:
            print("L'utilisateur n'a pas de compte social lié à Facebook")

    return render(request, 'index.html', locals())






