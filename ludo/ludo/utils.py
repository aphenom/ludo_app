from decimal import Decimal
import string
import random
from django.conf import settings
from django.urls import resolve
from django.utils import timezone
from django.db.models import Q, Sum

from core.models import Config, TauxCommission, TauxTransaction
from player.models import HistoriqueNotification, Participation, Profil, Transaction
from .enum import Genre, TypeTransaction

import requests
import json

def ContextConfig(request):
    
    try:  
        config = Config.objects.filter(etat_validation=True, etat_suppression=False).first()  
    except:
        config = None

    user = request.user

    try:  
        my_current_url = resolve(request.path_info).url_name 
    except:
        my_current_url = None

    code_invitation = request.session.get('code_invitation', '')

    next = request.session.get('next', '')

    solde = Transaction.objects.filter(Q((Q(type=TypeTransaction.Retrait) | Q(type=TypeTransaction.Mise)), etat_suppression=False) 
                                       | Q((Q(type=TypeTransaction.Depot) | Q(type=TypeTransaction.Gain)), etat_validation=True)).aggregate(total=Sum('montant'))["total"]

    solde = solde if solde else 0

    minimum_depot = config.minimum_depot if config and config.minimum_depot else 100

    minimum_retrait = config.minimum_retrait if config and config.minimum_retrait else 1000

    profil = None
    complement_genre = ""
    if user.is_authenticated:
        try:
            # Récupérer les données de l'utilisateur à partir du modèle SocialAccount
            profil = Profil.objects.get(user=user)
            if profil.genre == Genre.Feminin:
                complement_genre = "e"
        except Profil.DoesNotExist:
            print("L'utilisateur n'a pas de compte social lié à Facebook")

    notifications_attentes = None
    if profil:
        notifications_attentes = HistoriqueNotification.objects.filter(profil=profil, etat_lecture=False, etat_validation=True, etat_suppression=False)

    partie_encours = None
    if profil:
        partie_encours = Participation.objects.filter(profil = profil, partie__etat_fin = False, partie__etat_validation=True, partie__etat_suppression=False, etat_fin=False, etat_exclusion=False, etat_validation=True, etat_suppression=False).first()


    return {
        'config' : config, 
        'profil' : profil, 
        'notifications_attentes' : notifications_attentes, 
        'complement_genre' : complement_genre, 
        'my_current_url' : my_current_url, 
        'code_invitation' : code_invitation, 
        'next' : next,
        'solde' : solde,
        'minimum_depot' : minimum_depot,
        'minimum_retrait' : minimum_retrait,
        'partie_encours' : partie_encours
        }      
    # return {'config' : config, 'costum_parallax' : costum_parallax, 'my_current_url':my_current_url, 'notification_messages':notification_messages, 'gtag':settings.GTAG}      

def CurrentConfig():
    try:  
        return Config.objects.filter(etat_validation=True, etat_suppression=False).order_by("-pk").first()
    except:
        return None
    

def CurrentTauxCommission():
    return TauxCommission.objects.filter(etat_validation=True, etat_suppression=False).order_by("-pk").first()

def CurrentTauxTransaction():
    return TauxTransaction.objects.filter(etat_validation=True, etat_suppression=False).order_by("-pk").first()

def DetermineCagnotte(mise, nombre_participants, taux_commission):
    montant = None
    if taux_commission is None:
        taux_commission = 0
    montant = Decimal(mise*nombre_participants)*Decimal(1-(taux_commission/100))
    return round(montant)
     
def DetermineCommission(mise, nombre_participants, taux_commission):
    montant = None
    if taux_commission is None:
        taux_commission = 0
    montant = Decimal(mise*nombre_participants)*Decimal(taux_commission/100)
    return round(montant)

def DetermineFraisGenere(montant, taux_frais):
    valeur = None
    if taux_frais is None:
        taux_frais = 0
    valeur = Decimal(montant)*Decimal(taux_frais/100)
    return round(valeur)


# notification wonderpush
WONDERPUSH_SECRET = CurrentConfig().notification_api_key if CurrentConfig() and CurrentConfig().notification_api_key else "YmM0MjAwMzE4ZjkxYWFmMjBiNGJkZTFjYWFkZDBjYmEzOTRlMGU0YmZiODEwNGU2MWEzMDY2M2ZlMGE2MjJiNQ"

def send_notification_to_device(installation_id, title, message):
    url = f"https://management-api.wonderpush.com/v1/deliveries?accessToken={WONDERPUSH_SECRET}"
    headers = {
        "accept": "text/plain",
        'Content-Type': 'application/json',
    }

    payload = {
        "targetInstallationIds": [installation_id],
        "notification": {
            "alert": {
                "title": title,
                "text": message
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    
    print(response.text)
    
    return response.json()

