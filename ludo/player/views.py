import json
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse
import requests

from core.models import Mise
from ludo.enum import TypeReferenceNotification, TypeTransaction, Visibilite
from ludo.utils import ContextConfig, CurrentConfig, CurrentTauxCommission, CurrentTauxTransaction, DetermineCagnotte, DetermineCommission, DetermineFraisGenere
from player.models import HistoriqueNotification, Participation, Partie, Profil, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cinetpay_sdk.s_d_k import Cinetpay
from django_dump_die.middleware import dd
import math
from django.db.models import Q, Sum
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib import messages


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
    
    response = reverse('player:player_dashboard')+"?tab=transaction-tab"

    config = CurrentConfig()

    montant_depot = int(montant)

    minimum_depot = int(config.minimum_depot) if config and config.minimum_depot else 100

    conformite = math.ceil(montant_depot / minimum_depot) * minimum_depot if montant_depot > 0 else minimum_depot

    if montant_depot == int(conformite):
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=request.user, etat_validation=True, etat_suppression=False)
            # Afficher les informations du compte social
            # print(profil)
        except Profil.DoesNotExist:
            raise Http404 # print("L'utilisateur n'a pas de compte social lié à Facebook")
            
        transaction = Transaction()
        transaction.config = config
        transaction.depot = montant_depot
        transaction.montant = montant_depot
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
    
    response = reverse('player:player_dashboard')+"?tab=transaction-tab"

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


def retrait(request, pays, canal, contact, montant, email):

    response = reverse('player:player_dashboard')+"?tab=withdraw-tab"

    config = CurrentConfig()

    solde = ContextConfig(request)['solde']  # Stocker le solde dans une variable pour éviter d'appeler plusieurs fois
    
    montant_retrait = int(montant)

    minimum_retrait = int(config.minimum_retrait) if config and config.minimum_retrait else 100

    conformite = math.ceil(montant_retrait / minimum_retrait) * minimum_retrait if montant_retrait > 0 else minimum_retrait

    # Vérifier si le profil a assez de solde pour le retrait
    if solde < montant_retrait:
        raise ValueError("Solde utilisateur insuffisant")

    if montant_retrait == int(conformite):
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=request.user, etat_validation=True, etat_suppression=False)
            # Afficher les informations du compte social
            # print(profil)
        except Profil.DoesNotExist:
            raise Http404 # print("L'utilisateur n'a pas de compte social lié à Facebook")
            
        transaction = Transaction()
        transaction.config = config
        transaction.contact_transaction = str(pays) + str(contact)
        transaction.retrait = montant_retrait
        transaction.montant = (-1)*montant_retrait
        transaction.frais_genere = DetermineFraisGenere(montant, CurrentTauxTransaction().taux if CurrentTauxTransaction() and CurrentTauxTransaction().taux else None)
        transaction.taux_frais_genere = CurrentTauxTransaction()
        transaction.etat_validation = False 
        transaction.description = "Retrait d'argent du compte"
        transaction.type = TypeTransaction.Retrait
        transaction.type_api = "Cinetpay"
        transaction.profil = profil
        transaction.save()

        apikey = config.transaction_api_key if config and config.transaction_api_key else "1121307539667c1e026ec794.68685186"
        apipassword = config.transaction_api_password if config and config.transaction_api_password else "password"
        site_id = config.transaction_api_id if config and config.transaction_api_id else "5874786"

        try:
            # connectons nous au service pour avoir le token
            url_login = "https://client.cinetpay.com/v1/auth/login"
            headers_login = {
                "accept": "text/plain",
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            payload_login = {
                "apikey": apikey,
                "password": apipassword,
            }
            response_login = requests.post(url_login, data=payload_login, headers=headers_login)
            data_login = response_login.json()
            token = data_login["data"]["token"]

            #creons un contact de transfert au cas où le numero n'existe pas deja dans la liste du service
            if token :
                url_contact = f"https://client.cinetpay.com/v1/transfer/contact?token={token}"
                headers_contact = {
                    "accept": "text/plain",
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
                payload_contact = {"data": json.dumps([
                    {
                        "prefix": "225",
                        "phone": "0707020400",
                        "name": "Test A",
                        "surname": "Test B AP",
                        "email": "test@madoha.com"
                    }
                ])} 
                response_contact = requests.post(url_contact, data=payload_contact, headers=headers_contact)
                data_contact = response_contact.json()
                # print(data_contact)

                #transferons l'argent au contact créé
                if data_contact["code"] == 0:
                    url_send = f"https://client.cinetpay.com/v1/transfer/money/send/contact?token={token}"
                    
                    headers_send = {
                        "accept": "text/plain",
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }

                    payload_send = {"data": json.dumps([
                        {
                            "prefix": str(pays),
                            "phone": str(contact),
                            "amount": montant_retrait,
                            "client_transaction_id": transaction.code,
                            "notify_url": reverse('player:player_retrait_callback',args=[transaction.code]),
                            #"payment_method": "http://yourdomain.com/transfer/notify",
                        }
                    ])} 

                    response_send = requests.post(url_send, data=payload_send, headers=headers_send)
                    data_send = response_send.json()
                    #dd(data_send)
                    print(data_send)

                    if data_send["code"] == 0:
                        response = reverse('player:player_dashboard')+"?tab=transaction-tab"

        except Exception as e:
            # Gérer les exceptions liées aux vérifications
            messages.error(request, str(e))  # Afficher le message d'erreur correspondant
            #return redirect('error_page')  # Rediriger vers une page d'erreur
            # dd(payload)

    return HttpResponseRedirect(response)


        
def retrait_callback(request, code):
    
    response = reverse('player:player_dashboard')+"?tab=transaction-tab"

    config = CurrentConfig()

    try:
        # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
        transaction = Transaction.objects.get(code=code)
        # Afficher les informations du compte social
        # print(profil)
    except Transaction.DoesNotExist:
       raise Http404 # print("L'utilisateur n'a pas de compte social lié à Facebook")

    apikey = config.transaction_api_key if config and config.transaction_api_key else "1121307539667c1e026ec794.68685186"
    apipassword = config.transaction_api_password if config and config.transaction_api_password else "password"
    site_id = config.transaction_api_id if config and config.transaction_api_id else "5874786"

    try:
        # connectons nous au service pour avoir le token
        url_login = "https://client.cinetpay.com/v1/auth/login"
        headers_login = {
            "accept": "text/plain",
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload_login = {
            "apikey": apikey,
            "password": apipassword,
        }
        response_login = requests.post(url_login, data=payload_login, headers=headers_login)
        data_login = response_login.json()
        token = data_login["data"]["token"]

        # verifions le transfert d'argent
        if token :
            url_check = f"https://client.cinetpay.com/v1/transfer/check/money?token={token}&client_transaction_id={code}"
            headers_check = {
                "accept": "text/plain",
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            response_check = requests.post(url_check, headers=headers_check)
            data_check = response_check.json()
            print(data_check)

            #transferons l'argent au contact créé
            if data_check["code"] == 0:
                transaction.operateur = data_check["data"][0]["operator"]
                if data_check["data"][0]["treatment_status"] == "VAL":
                    transaction.etat_validation = True
                    transaction.etat_suppression = False
                if data_check["data"][0]["treatment_status"] == "REJ":
                    transaction.etat_validation = False
                    transaction.etat_suppression = True
                    transaction.description = data_check["data"][0]["comment"]
                transaction.save()

    except Exception as e:
        # Gérer les exceptions liées aux vérifications
        messages.error(request, str(e))  # Afficher le message d'erreur correspondant
        #return redirect('error_page')  # Rediriger vers une page d'erreur
        # dd(payload)


    # print(retour)
    # JsonResponse(retour) 
    return HttpResponseRedirect(response)
