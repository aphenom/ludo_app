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
from .views import custom_login_redirect, facebook_login_with_state, index


urlpatterns = [

    path('', index, name='index'),

    # Django admin
    path('admin/', admin.site.urls),

    # path('facebook-login/', facebook_login_with_state, name='facebook_login_with_state'),
    
    path('accounts/login/', facebook_login_with_state, name='facebook_login_with_state'),

    path('accounts/login-redirect/', custom_login_redirect, name='custom_login_redirect'),
    
    # Rediriger la connexion normale vers Facebook
    # path('accounts/login/', custom_login_redirect),

    # Allauth URLs pour l'authentification
    path('accounts/', include('allauth.urls')),

    path('tinymce/', include('tinymce.urls')),

    path('player/', include('player.urls')),
]
