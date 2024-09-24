from decimal import Decimal
import string
import random
from django.conf import settings
from django.utils import timezone

from core.models import Config, TauxCommission, TauxTransaction


'''generateur code de referemce'''
def CodeGenerator(self, model, start_by_text, end_by_text):
    count = model.objects.filter(created_at__year=timezone.now().year, created_at__month=timezone.now().month, created_at__day=timezone.now().day).count()
    current_number = count + 1
    result = f"{start_by_text}{timezone.now().year}{timezone.now().month}{timezone.now().day}{random.choice(string.ascii_letters).upper()}{current_number:03d}"
    return result

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