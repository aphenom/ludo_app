from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise
from ludo.enum import Visibilite
from ludo.utils import CurrentConfig, CurrentTauxCommission, DetermineCagnotte, DetermineCommission
from player.models import Participation, Partie, Profil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def dashboard(request):

    return render(request, 'player/dashboard.html', locals())


#@login_required
def profil(request):

   # Récupérer l'utilisateur connecté
    user = request.user
    # Si l'utilisateur est authentifié via Facebook
    if user.is_authenticated:
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=user)

            partie_privee = Partie.objects.filter(organise_par=profil, visibilite = Visibilite.Privee, etat_demarrage = False, etat_validation=True, etat_suppression=False).first()

            participation_en_cours = Participation.objects.filter(partie__etat_fin = False, partie__etat_validation=True, partie__etat_suppression=False, etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False).first()
            
            participation_terminees = Participation.objects.filter(partie__etat_fin = True, partie__etat_validation=True, partie__etat_suppression=False, etat_fin=True, etat_validation=True, etat_suppression=False)
            
            if participation_en_cours:
                partie_en_cours = participation_en_cours.partie
            # Afficher les informations du compte social
            print(profil)
        except Profil.DoesNotExist:
            print("L'utilisateur n'a pas de compte social lié à Facebook")
            
    return render(request, 'player/profil.html', locals())




