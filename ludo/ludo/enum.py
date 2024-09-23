import pprint

#from django.core import serializers
from django.db import models
#from django.http import JsonResponse, HttpResponse


# iterable 
Situation = ( 
    ("RESIDENT", "RESIDENT"), 
    ("NON_RESIDENT", "NON RESIDENT"),
) 

Role = ( 
    ("NEANT", "NEANT"), 
    ("PAROISSIEN", "PAROISSIEN"),
    ("CHEF_CHRETIEN", "CHEF_CHRETIEN"),
    ("CHEF_SECTEUR", "CHEF_SECTEUR"),
    ("PRETRE", "PRETRE"),
    ("EVEQUE", "EVEQUE"),
) 

Assiduite = ( 
    ("ASSIDU", "ASSIDU"), 
    ("A_SUIVRE", "A SUIVRE"),
    ("NON_ASSIDU", "NON ASSIDU"),
) 



class Status(models.TextChoices):
    ACTIVE = 'ACTIVE'
    DESACTIVE = 'DESACTIVE'
    SUPPRIME = 'SUPPRIME'

class OptionYesNo(models.TextChoices):
    OUI = 'OUI'
    NON = 'NON'
    CHOISIR = ''

class Genre(models.TextChoices):
    Masculin = 'Masculin'
    Feminin = 'Féminin'  

class TypeTransaction(models.TextChoices):
    Depot = 'Dépôt'
    Retrait = 'Retrait'   
    Mise = 'Mise'   
    Gain = 'Gain'   

class Visibilite(models.TextChoices):
    Public = 'Public'
    Privee = 'Privée'  