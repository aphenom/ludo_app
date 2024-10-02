from decimal import Decimal
import string
import random
from django.conf import settings
from django.urls import resolve
from django.utils import timezone

from core.models import Config, TauxCommission, TauxTransaction


def ContextConfig(request):
    config = Config.objects.filter(etat_validation=True, etat_suppression=False).first() 

    try:  
        my_current_url = resolve(request.path_info).url_name 
    except:
        my_current_url = None

    code_invitation = request.session.get('code_invitation', '')

    next = request.session.get('next', '')

    solde = 0 

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
        'my_current_url' : my_current_url, 
        'code_invitation' : code_invitation, 
        'next' : next,
        'solde' : solde
        }      
    # return {'config' : config, 'costum_parallax' : costum_parallax, 'my_current_url':my_current_url, 'notification_messages':notification_messages, 'gtag':settings.GTAG}      



'''generateur code de referemce'''
def CodeGenerator(model, start_by_text, end_by_text):

    # Simuler un 'do-while' avec 'while True' et un 'break'
    while True:
        letters_and_digits = string.ascii_uppercase # + string.digits  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        code_letters = ''.join(random.choice(letters_and_digits) for _ in range(4))
        code = str(start_by_text) + str(code_letters) + str(end_by_text)
        count = model.objects.filter(code=code).count()
        if count > 0:
            pass
        else:
            return code
            

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
    montant = mise*nombre_participants*Decimal(1-(taux_commission/100))
    return round(montant)
     
def DetermineCommission(mise, nombre_participants, taux_commission):
    montant = None
    if taux_commission is None:
        taux_commission = 0
    montant = mise*nombre_participants*Decimal(taux_commission/100)
    return round(montant)