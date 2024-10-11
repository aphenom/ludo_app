import json
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse
import requests

from core.models import Mise
from ludo.enum import TypeReferenceNotification, TypeTransaction, Visibilite
from ludo.utils import CurrentConfig, CurrentTauxCommission, CurrentTauxTransaction, DetermineCagnotte, DetermineCommission, DetermineFraisGenere
from player.models import HistoriqueNotification, Participation, Partie, Profil, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cinetpay_sdk.s_d_k import Cinetpay
from django_dump_die.middleware import dd
import math
from django.db.models import Q, Sum
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma


@login_required
def dashboard(request):

    tab = request.GET.get('tab', None)

    participations = Participation.objects.filter(partie__etat_validation=True, partie__etat_suppression=False, etat_validation=True, etat_suppression=False)

    transactions = Transaction.objects.filter(
        Q((Q(type=TypeTransaction.Retrait) | Q(type=TypeTransaction.Mise)), etat_suppression=False) 
        | Q((Q(type=TypeTransaction.Depot) | Q(type=TypeTransaction.Gain)), etat_validation=True))

    return render(request, 'player/dashboard.html', locals())


@login_required
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


@login_required
def rechargement(request, montant):
    
    response = reverse('player:player_profil')+"?tab=transaction-tab"

    config = CurrentConfig()

    minimum_depot = int(config.minimum_depot) if config and config.minimum_depot else 100

    conformite = math.ceil(int(montant) / minimum_depot) * minimum_depot if int(montant) > 0 else minimum_depot

    if int(montant) == int(conformite):
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=request.user, etat_validation=True, etat_suppression=False)
            # Afficher les informations du compte social
            # print(profil)
        except Profil.DoesNotExist:
            raise Http404 # print("L'utilisateur n'a pas de compte social lié à Facebook")
            
        transaction = Transaction()
        transaction.config = config
        transaction.depot = montant
        transaction.montant = montant
        transaction.frais_genere = DetermineFraisGenere(montant, CurrentTauxTransaction().taux if CurrentTauxTransaction() and CurrentTauxTransaction().taux else None)
        transaction.taux_frais_genere = CurrentTauxTransaction()
        # a transformer en False en production
        transaction.etat_validation = True # a transformer en False en production
        transaction.description = "Rechargement du compte"
        transaction.type = TypeTransaction.Depot
        transaction.type_api = "Cinetpay"
        transaction.profil = profil
        transaction.save()

        apikey = config.transaction_api_key if config and config.transaction_api_key else "1121307539667c1e026ec794.68685186"
        site_id = config.transaction_api_id if config and config.transaction_api_id else "5874786"

        client = Cinetpay(apikey,site_id)
        data = { 
            'amount' : transaction.montant, #transaction.montant
            'currency' : "XOF",            
            'transaction_id' : transaction.code,  
            'description' : transaction.description,  
            'return_url' : reverse('player:player_rechargement_callback',args=[transaction.code]),
            'notify_url' : reverse('player:player_rechargement_callback',args=[transaction.code]), 
            'customer_name' : profil.nom,                              
            'customer_surname' : profil.prenom,       
        }  
        
        retour = client.PaymentInitialization(data)
        # dd(retour) # type: ignore
        if retour and (retour["code"] == '201' or retour["code"] == '00'):
            response = retour["data"]["payment_url"]
        # print(retour)
        # return JsonResponse(retour) 
    return HttpResponseRedirect(response)


def rechargement_callback(request, code):
    
    response = reverse('player:player_profil')+"?tab=transaction-tab"

    config = CurrentConfig()

    try:
        # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
        transaction = Transaction.objects.get(code=code)
        # Afficher les informations du compte social
        # print(profil)
    except Transaction.DoesNotExist:
       raise Http404 # print("L'utilisateur n'a pas de compte social lié à Facebook")

    if request.method == 'POST':
        #transaction.etat_validation = True
        transaction.contact_transaction = str(request.POST.get('cpm_phone_prefixe',"")) + str(request.POST.get('cel_phone_num')) 
        transaction.operateur = str(request.POST.get('payment_method',"")) 
        transaction.description = str(request.POST.get('cpm_error_message',transaction.description)) 

    apikey = config.transaction_api_key if config and config.transaction_api_key else "1121307539667c1e026ec794.68685186"
    site_id = config.transaction_api_id if config and config.transaction_api_id else "5874786"

    client = Cinetpay(apikey,site_id)
    #transaction_id = "XXXXXX"

    retour = client.TransactionVerfication_trx(code)
    
    #succes
    if retour and retour["code"] == '00' and transaction.etat_validation is False:
        transaction.etat_validation = True
        transaction.etat_suppression = False

        notification = HistoriqueNotification(
            profil=transaction.profil,
            objet = transaction.description,
            message = "Ton réchargement de {} {} a été effectué avec succès !".format(intcomma(floatformat(transaction.montant,-2)), config.currency if config and config.currency else "FCFA"),
            type_reference = TypeReferenceNotification.Transaction,
            id_reference = transaction.pk
        )
        notification.save()
    
    #echec
    if retour and retour == "600":
        transaction.etat_validation = False
        transaction.etat_suppression = True
    
    transaction.save()

    # print(retour)
    # JsonResponse(retour) 
    return HttpResponseRedirect(response)


def retrait(request, contact, montant):

    config = CurrentConfig()

    apikey = config.transaction_api_key if config and config.transaction_api_key else "1121307539667c1e026ec794.68685186"
    site_id = config.transaction_api_id if config and config.transaction_api_id else "5874786"

    url = "https://client.cinetpay.com/v1/auth/login"

    headers = {
        "accept": "text/plain",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    payload = {
        "apikey": apikey,
        "password": "password",
    }

    response = requests.post(url, data=payload, headers=headers)
    
    data = response.json()

    token = data["data"]["token"]

    url = f"https://client.cinetpay.com/v1/transfer/contact?token={token}"
    
    headers = {
        "accept": "text/plain",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    payload = {"data": json.dumps([{
    "prefix": "225",
    "phone": "0707020400",
    "name": "Test A",
    "surname": "Test B AP",
    "email": "test@madoha.com"
    }])
    } 

    # dd(payload)

    response = requests.post(url, data=payload, headers=headers)
    
    data = response.json()
    
    if data["code"] == 0:
        url = f"https://client.cinetpay.com/v1/transfer/money/send/contact?token={token}"
        
        headers = {
            "accept": "text/plain",
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        payload = {"data": json.dumps([{
        "prefix": "225",
        "phone": "0707020400",
        "amount": 500,
        "client_transaction_id": "TEST-ID1",
        "notify_url": "http://yourdomain.com/transfer/notify",
        }])
        } 

        # dd(payload)

        response = requests.post(url, data=payload, headers=headers)
        

    #dd(response)

    dd(response.json())
    
    return response.json()


