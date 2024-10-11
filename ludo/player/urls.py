from django.urls import path

from . import views # import views so we can use them in urls.

app_name = 'player'
urlpatterns = [
    path('dashboard/', views.dashboard, name='player_dashboard'),
    path('profil/', views.profil, name='player_profil'),
    path('rechargement/<str:montant>/', views.rechargement, name='player_rechargement'),
    path('rechargement_callback/<str:code>/', views.rechargement_callback, name='player_rechargement_callback'),
    path('retrait/<str:contact>/<str:montant>/', views.retrait, name='player_retrait'),
]