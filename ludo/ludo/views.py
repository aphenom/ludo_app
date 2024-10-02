from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise
from ludo.enum import Visibilite
from ludo.utils import ContextConfig, CurrentConfig, CurrentTauxCommission, DetermineCagnotte, DetermineCommission
from player.models import Participation, Partie, Profil
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_dump_die.middleware import dd
from urllib.parse import urlencode
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma


def facebook_login_with_state(request):
    # Ajouter des paramètres que tu souhaites passer dans l'URL de redirection
    next_url = request.GET.get('next', ContextConfig(request)['next'])
    code_invitation = request.GET.get('code_invitation', ContextConfig(request)['code_invitation'])

    request.session['next'] = next_url
    request.session['code_invitation'] = code_invitation

    # custom_variable = 'custom_value'  # Variable que tu veux passer
    # custom_variable = request.GET.get('custom_variable', custom_variable)
    state = urlencode({'next': next_url, 'code_invitation': code_invitation})
    
    # Exemple d'utilisation : récupérer l'utilisateur connecté via Facebook
    facebook_login_url = f'/accounts/facebook/login/?{state}'
    return redirect(facebook_login_url)


#@login_required
def index(request):

    # Récupérer les paramètres de `state` dans la requête
    next_url = request.GET.get('next', ContextConfig(request)['next'])
    code_invitation = request.GET.get('code_invitation', ContextConfig(request)['code_invitation'])

    # Récupérer l'utilisateur connecté
    user = request.user

    # a supprimer en prod
    user = User.objects.all().first()
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

    # Exemple d'utilisation : récupérer l'utilisateur connecté via Facebook
    if user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=user, provider='facebook')
            # Tu peux accéder aux données du profil Facebook de l'utilisateur ici
            facebook_data = social_account.extra_data
            name = facebook_data.get('name')
            email = facebook_data.get('email')
            id_facebook = facebook_data.get('id')
            nom = facebook_data.get('last_name')
            prenom = facebook_data.get('first_name')

            # Vérifier si un profil avec cet email existe
            try:
                profil = Profil.objects.get(user=user)
                # Mettre à jour le profil existant si besoin
                if email and email is not "" and email != profil.email:
                    profil.email = email
                    profil.save()

                if nom and nom is not "" and nom != profil.nom:   
                    profil.nom = nom
                    profil.save()

                if prenom and prenom is not "" and prenom != profil.prenom:
                    profil.prenom = prenom
                    profil.save()
            except Profil.DoesNotExist:
                
                # Créer un nouveau profil si l'utilisateur est nouveau
                profil = Profil()
                profil.user=user
                profil.id_facebook=id_facebook
                profil.nom=nom
                profil.prenom=prenom
                profil.email=email
                profil.date_validation=timezone.now()

                if code_invitation and code_invitation is not "":
                    profil.code_invite_par = code_invitation
                    invite_par = profil.objects.filter(code=code_invitation, etat_suppression=False).first()
                    if invite_par:
                        profil.invite_par = invite_par
                
                profil.save()

            # Ajoute ici tes traitements en fonction de `custom_variable` ou des données utilisateur
        except SocialAccount.DoesNotExist:
            return HttpResponse("Erreur: aucun compte Facebook trouvé.", status=404)

        if 'next' in request.session:
                del request.session['next']
        if 'code_invitation' in request.session:
                del request.session['code_invitation']
   
    # dd(request)
    # determinons l'ensemble des mises possibles
    liste_mises = Mise.objects.filter(etat_validation=True, etat_suppression=False)

    choix_parties_privees = []
    
    # parcourons les mises pour creer des parties ou recuperons celles en attentes en fonction
    for mise in liste_mises:
        for nombre_participants in range(mise.nombre_minimum,5):
            if nombre_participants >= 2 and nombre_participants <= 4:

                #montant
                montant_cagnotte = DetermineCagnotte(mise.montant, nombre_participants, CurrentTauxCommission().taux if CurrentTauxCommission() and CurrentTauxCommission().taux else None)
                montant_commission = DetermineCommission(mise.montant, nombre_participants, CurrentTauxCommission().taux if CurrentTauxCommission() and CurrentTauxCommission().taux else None)
                
                #config 
                config = CurrentConfig()
                
                #choix pour creation de partie
                choix_parties_privees.append({
                    "mise":mise,
                    "nombre_participants":nombre_participants,
                    "montant_cagnotte":montant_cagnotte,
                    "montant_commission":montant_commission,
                    "texte_option":"Mise : {} {} | {} : {} | Gain : {} {}".format(intcomma(floatformat(mise.montant,-2)), config.currency if config and config.currency else "", "1 contre 1" if nombre_participants < 3 else "Joueurs", nombre_participants, intcomma(floatformat(montant_cagnotte,-2)), config.currency if config and config.currency else ""),
                    "valeur_option":"Mise : {} {} | {} : {} | Gain : {} {}".format(intcomma(floatformat(mise.montant,-2)), config.currency if config and config.currency else "", "1 contre 1" if nombre_participants < 3 else "Joueurs", nombre_participants, intcomma(floatformat(montant_cagnotte,-2)), config.currency if config and config.currency else "")
                })

                #gerons les parties par defaut
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
                    partie.config = config
                    partie.delai_tour = config.delai_tour if config and config.delai_tour else None
                    partie.mise = mise
                    partie.montant_mise = mise.montant
                    partie.nombre_participants = nombre_participants
                    partie.montant_cagnotte = montant_cagnotte
                    partie.montant_commission = montant_commission
                    partie.taux_comission = CurrentTauxCommission()
                    partie.save()
    
    #trions les choix pour les parties privees 
    choix_parties_privees_triees = sorted(choix_parties_privees, key=lambda x: x['montant_cagnotte'], reverse=True)
    # dd(choix_parties_privees)

    # recuperons les parties valides pretes a recevoir des joueurs
    liste_parties = Partie.objects.filter(visibilite = Visibilite.Public, etat_demarrage = False, etat_validation=True, etat_suppression=False)

    # partie privee pour utilisateur connecté
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

    if next_url != '/' and next_url != '':
        return redirect(next_url)
    
    return render(request, 'index.html', locals())






