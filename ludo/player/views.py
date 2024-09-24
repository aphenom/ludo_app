from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from core.models import Mise
from ludo.enum import Visibilite
from ludo.utils import CurrentConfig, CurrentTauxCommission, DetermineCagnotte, DetermineCommission
from player.models import Partie


def dashboard(request):

    return render(request, 'player/dashboard.html', locals())


def profil(request):

    return render(request, 'player/profil.html', locals())




