import json
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse

from core.models import Mise
from .enum import TypeTransaction, Visibilite
from .utils import ContextConfig, CurrentConfig, CurrentTauxCommission, DetermineCagnotte, DetermineCommission, send_notification_to_device
from player.models import Participation, Partie, Profil, Transaction, Visiteur
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_dump_die.middleware import dd
from urllib.parse import urlencode
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# fonctiannilite de connexion facebook
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
# index de la plateforme
def index(request):

    # send_notification_to_device("6d37c0e08f34c443388e8f32005290525e9632a7", "welcome", "to you ohhh")
    # 6735cbb21c7c97cdebc3110ead81e0c81daa3604 mac
    # print("notif")

    # Récupérer les paramètres de `state` dans la requête
    next_url = request.GET.get('next', ContextConfig(request)['next'])
    code_invitation = request.GET.get('code_invitation', ContextConfig(request)['code_invitation'])
    
    # pour rejoindre une partie privee /?rejoindre_partie_code=code
    rejoindre_partie_code = request.GET.get('rejoindre_partie_code', "")
    
    # pour rejoindre une partie privee /?public_partie_code=code
    public_partie_code = request.GET.get('public_partie_code', "")

    # Récupérer l'utilisateur connecté
    user = request.user

    # a supprimer en prod
    user = User.objects.all().first()
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

    # Exemple d'utilisation : récupérer l'utilisateur connecté via Facebook
    if user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=user, provider='facebook')
            checking_user(user, social_account, code_invitation)

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

    # parcourons les mises pour creer des parties ou recuperons celles en attentes en fonction et determinons les choix possibles pour les parties privees
    choix_parties_privees = generation_parties(request)
        
    #trions les choix pour les parties privees 
    choix_parties_privees_triees = sorted(choix_parties_privees, key=lambda x: x['montant_cagnotte'], reverse=True)
    # dd(choix_parties_privees)

    # recuperons les parties valides pretes a recevoir des joueurs
    liste_parties = Partie.objects.filter(visibilite = Visibilite.Public, etat_demarrage = False, etat_validation=True, etat_suppression=False).order_by("-montant_cagnotte")

    # partie privee pour utilisateur connecté
    # Si l'utilisateur est authentifié via Facebook
    if user.is_authenticated:
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=user)

            partie_privee = Partie.objects.filter(organise_par=profil, visibilite = Visibilite.Privee, etat_demarrage = False, etat_validation=True, etat_suppression=False).first()

            participation_en_cours = Participation.objects.filter(profil = profil, partie__etat_fin = False, partie__etat_validation=True, partie__etat_suppression=False, etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False).first()
            
            if participation_en_cours:
                partie_en_cours = participation_en_cours.partie
                return redirect(reverse('index_partie', args=[timezone.now().strftime('%d%m%Y%H%M%S%f'), partie_en_cours.code]))
            
            # Afficher les informations du compte social
            # print(profil)


        except Profil.DoesNotExist:
            print("L'utilisateur n'a pas de compte social lié à Facebook")

    if next_url != '/' and next_url != '':
        return redirect(next_url)
    
    # messages.error(request, "La partie n'existe pas.")
    
    return render(request, 'index.html', locals())


'''Avoir une partie privee via code'''
@login_required
def api_get_partie_privee_via_by_code(request):
    # dd(request)
    data = {}
    if request.method == 'GET':
        # no need to do this
        # request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
        code_partie_privee = request.GET.get('code_partie_privee')  
        # dd(code_partie_privee)   
        partie = Partie.objects.filter(code=code_partie_privee, etat_demarrage = False, etat_validation=True, etat_suppression=False, visibilite=Visibilite.Privee).first() #,visibilite-=Visibilite.Privee) 
        # answers_list = Answer.objects.filter(is_active=True, question__pub__uuid__exact=uuid).values()
        config = CurrentConfig()
        if partie:
            data = {
                'mise': partie.montant_mise,
                'nombre_participants': partie.nombre_participants,
                'gain': partie.montant_cagnotte,
                'minimum_depot': config.minimum_depot if config and config.minimum_depot else 100,
                'solde': ContextConfig(request)['solde'],
                'currency': config.currency if config and config.currency else "FCFA",
                # 'answers': list(answers_list),
            }
    return JsonResponse(data) 


# misons afin de participer a une partie
@login_required
def participer_partie(request, leurre, type, code):
    config = CurrentConfig()
    profil = ContextConfig(request)['profil']  # Assurez-vous que 'profil' existe dans ContextConfig
    solde = ContextConfig(request)['solde']  # Stocker le solde dans une variable pour éviter d'appeler plusieurs fois
    response = reverse('index')
    try:
        # Récupérer les données de la partie
        partie = Partie.objects.get(
            code=code, visibilite=type, etat_demarrage=False, 
            etat_validation=True, etat_suppression=False
        )

        # Vérifier s'il y a des places disponibles
        if partie.places_disponibles <= 0:
            raise ValueError("Nombre de participants atteint")

        # Vérifier si le profil a assez de solde pour la mise
        if solde < partie.montant_mise:
            raise ValueError("Solde insuffisant")

        # Vérifier que l'utilisateur ne participe pas déjà à une autre partie en cours
        participation_en_cours = Participation.objects.filter(
            profil=profil, 
            partie__etat_fin=False, partie__etat_validation=True, partie__etat_suppression=False, 
            etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
        ).first()

        if participation_en_cours:
            raise ValueError("Vous participez déjà à une autre partie en cours.")

        # Si tout est bon, créer une nouvelle participation
        participation = Participation(
            partie=partie,
            profil=profil
        )
        participation.save()

        # Créer une transaction de mise
        transaction_mise = Transaction(
            config=config,
            mise=partie.montant_mise,
            montant=(-1)*partie.montant_mise,
            etat_validation=True,
            description="Mise pour une partie",
            type=TypeTransaction.Mise,  # Assurez-vous que TypeTransaction.Mise est bien défini
            type_api="Système",
            partie=partie,
            profil=profil
        )
        transaction_mise.save()
        
        # Rediriger vers la page de la partie
        response = reverse('index_partie', args=[timezone.now().strftime('%d%m%Y%H%M%S%f'), code])

    except Partie.DoesNotExist:
        # Gérer l'erreur si la partie n'existe pas
        messages.error(request, "La partie n'existe pas.")
        #return redirect('error_page')  # Redirigez vers une page d'erreur ou l'index si nécessaire

    except ValueError as e:
        # Gérer les exceptions liées aux vérifications
        messages.error(request, str(e))  # Afficher le message d'erreur correspondant
        #return redirect('error_page')  # Rediriger vers une page d'erreur

    return redirect(response)


# creons une partie privee et misons automatiquement afin de participer
@login_required
def creer_partie_privee(request, nombre_participants, leurre, montant_mise):
    
    config = CurrentConfig()
    profil = ContextConfig(request)['profil']  # Assurez-vous que 'profil' existe dans ContextConfig
    solde = ContextConfig(request)['solde']  # Stocker le solde dans une variable pour éviter d'appeler plusieurs fois
    response = reverse('index')
    montant_mise = int(montant_mise)
    nombre_participants = int(nombre_participants)
    montant_cagnotte = DetermineCagnotte(montant_mise, nombre_participants, CurrentTauxCommission().taux if CurrentTauxCommission() and CurrentTauxCommission().taux else None)
    montant_commission = DetermineCommission(montant_mise, nombre_participants, CurrentTauxCommission().taux if CurrentTauxCommission() and CurrentTauxCommission().taux else None)

    try:
        # Récupérer la mise correspondante
        mise = Mise.objects.get(
            montant=montant_mise, nombre_minimum__lte=nombre_participants, 
            etat_validation=True, etat_suppression=False
        )

        # Vérifier si le profil a assez de solde pour la mise
        if solde < montant_mise:
            raise ValueError("Solde insuffisant")

        # Vérifier que l'utilisateur ne participe pas déjà à une autre partie en cours
        participation_en_cours = Participation.objects.filter(
            profil=profil, 
            partie__etat_fin=False, partie__etat_validation=True, partie__etat_suppression=False, 
            etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
        ).first()

        if participation_en_cours:
            raise ValueError("Vous participez déjà à une autre partie en cours.")

        # Si tout est bon, créer une nouvelle partie puis une participation
        partie = Partie(
            config = config,
            delai_tour = config.delai_tour if config and config.delai_tour else None,
            mise = mise,
            montant_mise = montant_mise,
            nombre_participants = nombre_participants,
            montant_cagnotte = montant_cagnotte,
            montant_commission = montant_commission,
            taux_comission = CurrentTauxCommission(),
            visibilite = Visibilite.Privee,
            organise_par = profil
        )
        partie.save()
            
        participation = Participation(
            partie=partie,
            profil=profil
        )
        participation.save()

        # Créer une transaction de mise
        transaction_mise = Transaction(
            config=config,
            mise=montant_mise,
            montant=(-1)*montant_mise,
            etat_validation=True,
            description="Mise pour une partie",
            type=TypeTransaction.Mise,  # Assurez-vous que TypeTransaction.Mise est bien défini
            type_api="Système",
            partie=partie,
            profil=profil
        )
        transaction_mise.save()
        
        # Rediriger vers la page de la partie
        response = reverse('index_partie', args=[timezone.now().strftime('%d%m%Y%H%M%S%f'), partie.code])

    except Mise.DoesNotExist:
        # Gérer l'erreur si la partie n'existe pas
        messages.error(request, "Cette mise n'est pas possible.")
        #return redirect('error_page')  # Redirigez vers une page d'erreur ou l'index si nécessaire

    except ValueError as e:
        # Gérer les exceptions liées aux vérifications
        messages.error(request, str(e))  # Afficher le message d'erreur correspondant
        #return redirect('error_page')  # Rediriger vers une page d'erreur

    return redirect(response)


# accedons a la partie avec legitimite
@login_required
def index_partie(request, leurre, code):
    config = CurrentConfig()
    profil = ContextConfig(request)['profil']
    try:
        # Récupérer la partei
        partie = Partie.objects.get(
            code = code, etat_fin = False, 
            etat_validation=True, etat_suppression=False
            )
        
        # verifions qu'il participe a la partie en cours
        participation_en_cours_match = Participation.objects.filter(
            profil = profil, 
            partie = partie, 
            etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
            ).first()
        
        # ici tout est bon il accede à l'interface passé toutes les vérifications donc peut participer
        if participation_en_cours_match:
            return render(request, 'index_partie.html', locals())

        raise ValueError("Problème de concordance.")

    except Partie.DoesNotExist:
       messages.error(request, "La partie n'exsite pas.")
    
    except ValueError as e:
        # Gérer les exceptions liées aux vérifications
        messages.error(request, str(e))  # Afficher le message d'erreur correspondant
        #return redirect('error_page')  # Rediriger vers une page d'erreur
    
    return redirect(reverse('index'))


# checking servant lorsque le joueur attend le demarrage du jeu
@login_required
def check_participation_et_partie(request, code_partie):

    response_data = {}

    peut_supprimer_participation = False

    profil = ContextConfig(request)['profil']  # Si le profil est lié à l'utilisateur
    
    # Vérification de la participation en cours
    participation_en_cours = Participation.objects.filter(
        profil=profil, 
        partie__code=code_partie,
        etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
    ).first()

    if participation_en_cours is None:
        return JsonResponse(response_data)
    
    # Récupération de la partie en cours
    partie_en_cours = Partie.objects.filter(
        pk=participation_en_cours.partie.pk,
        etat_fin=False, 
        etat_validation=True, 
        etat_suppression=False
    ).first()

    if partie_en_cours is None:
        return JsonResponse(response_data)

    # dernier membre ayant rejoint la partie pour voir le delais d'attente pour possible retrait
    last_participation = Participation.objects.filter(
        partie=partie_en_cours,
        etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
    ).order_by("-pk")
    if partie_en_cours.visibilite == Visibilite.Public:
        difference_delais = timezone.now() - last_participation.first().date_creation
        temps_derniere_participation = difference_delais.total_seconds() / 60
        if temps_derniere_participation >= 5:
            peut_supprimer_participation = True
    else:
        if partie_en_cours.organise_par != profil:
            difference_delais = timezone.now() - last_participation.first().date_creation
            temps_derniere_participation = difference_delais.total_seconds() / 60
            if temps_derniere_participation >= 5:
                peut_supprimer_participation = True
        else:
            if last_participation.count() == 1:
                    peut_supprimer_participation = True
    
    # Structure de la réponse
    response_data = {
        'participation_en_cours': True,
        'partie_en_cours': True,
        'partie_etat_demarrage': partie_en_cours.etat_demarrage,
        'places_disponibles': partie_en_cours.places_disponibles,
        'peut_supprimer_participation': peut_supprimer_participation
    }

    return JsonResponse(response_data)


# annuler participation au jeu quand c'est possible
@login_required
def annuler_participation(request, code_partie):

    peut_supprimer_participation = False

    profil = ContextConfig(request)['profil']  # Si le profil est lié à l'utilisateur

    config = CurrentConfig()
    
    # Vérification de la participation en cours
    participation_en_cours = Participation.objects.filter(
        profil=profil, 
        partie__code=code_partie,
        etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
    ).first()

    if participation_en_cours is None:
        return redirect(reverse('index'))
    
    # Récupération de la partie en cours
    partie_en_cours = Partie.objects.filter(
        pk=participation_en_cours.partie.pk,
        etat_demarrage=False, 
        etat_fin=False, 
        etat_validation=True, 
        etat_suppression=False
    ).first()

    if partie_en_cours is None:
        return redirect(reverse('index'))

    # dernier membre ayant rejoint la partie pour voir le delais d'attente pour possible retrait
    last_participation = Participation.objects.filter(
        partie=partie_en_cours,
        etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False
    ).order_by("-pk")
    if partie_en_cours.visibilite == Visibilite.Public:
        difference_delais = timezone.now() - last_participation.first().date_creation
        temps_derniere_participation = difference_delais.total_seconds() / 60
        if temps_derniere_participation >= 5:
            peut_supprimer_participation = True
    else:
        if partie_en_cours.organise_par != profil:
            difference_delais = timezone.now() - last_participation.first().date_creation
            temps_derniere_participation = difference_delais.total_seconds() / 60
            if temps_derniere_participation >= 5:
                peut_supprimer_participation = True
        else:
            if last_participation.count() == 1:
                    peut_supprimer_participation = True

    # tous les feux sont au vert on supprime la partie
    if peut_supprimer_participation == True:
        participation_en_cours.etat_validation = False
        participation_en_cours.etat_suppression = True
        participation_en_cours.save()
        # remboursons la mise
        transaction_mise = Transaction(
            config=config,
            depot=partie_en_cours.montant_mise,
            montant=partie_en_cours.montant_mise,
            etat_validation=True,
            description="Remboursement de mise pour une participation annulée.",
            type=TypeTransaction.Depot,  # Assurez-vous que TypeTransaction.Mise est bien défini
            type_api="Système",
            partie=partie_en_cours,
            profil=profil
        )
        transaction_mise.save()

    return redirect(reverse('index'))


# permet de generer des parties pour l'utilisateur et accessible pour tout le reseau
def generation_parties(request):
    
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
                    "texte_option":"Mise : {} {} | {} | Gain : {} {}".format(intcomma(floatformat(mise.montant,-2)), config.currency if config and config.currency else "FCFA", "1 contre 1" if nombre_participants < 3 else "Joueurs : "+str(nombre_participants), intcomma(floatformat(montant_cagnotte,-2)), config.currency if config and config.currency else "FCFA"),
                    "valeur_option":"{};{};{};{};{}".format(mise.montant, nombre_participants, montant_cagnotte, ContextConfig(request)['solde'], config.minimum_depot if config and config.minimum_depot else 100)
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

    return choix_parties_privees


# gestion de la connexion du bon profil en fonction de facebook
def checking_user(user, social_account, code_invitation):
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
        if email and email != "" and email != profil.email:
            profil.email = email
            profil.save()

        if nom and nom != "" and nom != profil.nom:   
            profil.nom = nom
            profil.save()

        if prenom and prenom != "" and prenom != profil.prenom:
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

        if code_invitation and code_invitation != "":
            profil.code_invite_par = code_invitation
            invite_par = profil.objects.filter(code=code_invitation, etat_suppression=False).first()
            if invite_par:
                profil.invite_par = invite_par
            else:
                profil.code_invite_par = ""
        
        profil.save()    


# enregistrement de l'appareil du visiteur """"
@csrf_exempt
def register_device(request):
    if request.method == "POST":
        try:
            # Charger le corps de la requête en tant que JSON
            data = json.loads(request.body)
            installation_id = data.get("installation_id")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if installation_id:
            # Vérifiez si cet identifiant d'appareil existe déjà
            visitor, created = Visiteur.objects.get_or_create(
                visiteur_id=installation_id,
                profil=ContextConfig(request)['profil']
            )

            if created:
                visitor.save()
                return JsonResponse({'message': 'Device Installation ID enregistré.'}, status=200)
            else:
                return JsonResponse({'message': 'Device Installation ID déjà existant.'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def faq(request):
    return render(request, 'player/invitation.html', locals())


def privacy(request):
    return render(request, 'player/invitation.html', locals())


def cgu(request):
    return render(request, 'player/invitation.html', locals())

#supprimer en prod
def annuler(request):
    user = request.user
    if user.is_authenticated:
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=user)

            participation_en_cours = Participation.objects.filter(profil = profil, partie__etat_fin = False, partie__etat_validation=True, partie__etat_suppression=False, etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False)
            
            for participation in participation_en_cours:
                participation.etat_exclusion = True
                participation.save()
            return redirect(reverse('index'))
        except Profil.DoesNotExist:
            print("L'utilisateur n'a pas de compte social lié à Facebook")