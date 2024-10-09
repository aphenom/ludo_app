import datetime
from django import template

from ludo.enum import Genre
from ludo.utils import ContextConfig
from player.models import Participation

register = template.Library()


@register.simple_tag
def participation_state(id_participation, state_type):
    participation = Participation.objects.get(id=id_participation)
    libelle = ""
    couleur = ""
    if participation.etat_validation:
        libelle = "En attente"
        couleur = "warning"
    if participation.etat_demarrage:
        libelle = "En cours"
        couleur = "warning"
    if participation.etat_fin:
        libelle = "Echec"
        couleur = "danger"
    if participation.etat_suppression:
        libelle = "Annulation"
        couleur = "default"
    if participation.etat_exclusion:
        libelle = "Exclusion"
        couleur = "danger"
    if participation.etat_victoire:
        libelle = "Victoire"
        couleur = "success"
    if state_type == "libelle":
        return libelle
    else: 
        return couleur