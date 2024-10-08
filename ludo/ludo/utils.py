from decimal import Decimal
import string
import random
from django.conf import settings
from django.urls import resolve
from django.utils import timezone
from django.db.models import Q, Sum

from core.models import Config, TauxCommission, TauxTransaction
from player.models import HistoriqueNotification, Profil, Transaction
from .enum import Genre, TypeTransaction


def ContextConfig(request):
    
    config = Config.objects.filter(etat_validation=True, etat_suppression=False).first() 
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
        
    #print(solde)
    """ 
    if config.parallax and hasattr(config.parallax, 'url'):
        costum_parallax = config.parallax.url
    else:
        costum_parallax = static('images/login/login.jpg') 

    if request.user.is_authenticated:
        try:
            company = Company.objects.get(user=request.user)
            notification_messages = Message.objects.filter(company=company, submessage__isnull=True, is_readed=False, is_active=True).order_by("-created_at")
        except Company.DoesNotExist:
            notification_messages = None
        try:
            member = Member.objects.get(user=request.user)
            notification_messages = Message.objects.filter(member=member, submessage__isnull=True, is_readed=False, is_active=True).order_by("-created_at")
        except Member.DoesNotExist:
            if notification_messages == None:
                notification_messages = None
        test_message = User.objects.filter(pk=request.user.pk, groups__name='message').exists()        
        if request.user.is_staff == True and (test_message or request.user.is_superuser):
            notification_messages = Message.objects.filter(Q(submessage__isnull=True, is_active=True, is_from_user=True, is_noreply=False)).order_by("-created_at")         
    else:
        notification_messages = None
    """
    return {
        'config' : config, 
        'profil' : profil, 
        'notifications_attentes' : notifications_attentes, 
        'complement_genre' : complement_genre, 
        'my_current_url' : my_current_url, 
        'code_invitation' : code_invitation, 
        'next' : next,
        'solde' : solde
        }      
    # return {'config' : config, 'costum_parallax' : costum_parallax, 'my_current_url':my_current_url, 'notification_messages':notification_messages, 'gtag':settings.GTAG}      

def CurrentConfig():
    return Config.objects.filter(etat_validation=True, etat_suppression=False).order_by("-pk").first()

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