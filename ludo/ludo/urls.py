"""
URL configuration for ludo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import api_get_partie_privee_via_by_code, creer_partie_privee, facebook_login_with_state, index, index_partie, participer_partie, register_device


urlpatterns = [

    path('', index, name='index'),

    # Django admin
    path('admin/', admin.site.urls),

    
    path('participer_partie/<str:leurre>/<str:type>/<str:code>/', participer_partie, name='participer_partie'),
    
    path('creer_partie_privee/<str:nombre_participants>/<str:leurre>/<str:montant_mise>/', creer_partie_privee, name='creer_partie_privee'),
    
    path('index_partie/<str:leurre>/<str:code>/', index_partie, name='index_partie'),


    # path('facebook-login/', facebook_login_with_state, name='facebook_login_with_state'),
    
    path('accounts/login/', facebook_login_with_state, name='facebook_login_with_state'),
    
    path('api/api_get_partie_privee_via_by_code/', api_get_partie_privee_via_by_code, name='api_get_partie_privee_via_by_code'),
    
    path('api/register_device/', register_device, name='register_device'),

    # path('accounts/facebook/login/callback/', custom_login_redirect, name='custom_login_redirect'),

    # Rediriger la connexion normale vers Facebook
    # path('accounts/login/', custom_login_redirect),

    # Allauth URLs pour l'authentification
    path('accounts/', include('allauth.urls')),

    path('tinymce/', include('tinymce.urls')),

    path('player/', include('player.urls')),
]
