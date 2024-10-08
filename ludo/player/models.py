from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random  
import string 
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField
from cities_light.models import Country
from core.models import Config, Mise, TauxCommission, TauxTransaction
from ludo.enum import Genre, TypeTransaction, Visibilite

# Create your models here.

class Profil(models.Model):

    code = models.CharField(max_length=25, unique=True, editable=False)
    id_facebook = models.CharField(max_length=25, unique=True, editable=False)
    nom = models.CharField('nom', max_length=255, null=True, blank=True)
    prenom = models.CharField('prénom(s)', max_length=255, null=True, blank=True)
    genre = models.CharField(max_length=20, choices=Genre, null=True, blank=True, verbose_name = "genre")
    contact = PhoneNumberField("numéro principal", null=True, blank=True)
    contact_retrait = PhoneNumberField("numéro retrait", null=True, blank=True)
    email = models.EmailField("email", max_length=100, null=True, blank=True, unique=True)
    pays_residence = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="pays_profils", related_query_name="pays_profil", verbose_name = "pays")
    photo = models.FileField(upload_to='uploaded_media/photo_player', verbose_name="photo", null=True, blank=True)
    
    code = models.CharField(max_length=25, unique=True, editable=False)
    code_invite_par = models.CharField(max_length=25, null=True, blank=True)

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)
    
    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.DateTimeField('état suppression', default=False, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_profil', verbose_name = "profil")
    modifie_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='modifie_profils', related_query_name="modifie_profil", verbose_name = "modifié par")
    invite_par = models.ForeignKey('self', models.SET_NULL, related_name="invitation_profils", related_query_name="invitation_profil", verbose_name="invité par", null=True, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "profil"  
    
    def __str__(self):
        return (self.code + ' - ' + self.nom + ' ' + self.prenom)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.code = timezone.now().strftime('%d%m%Y%H%M%S%f')
            # self.email = self.user.email
            # phone = PhoneNumber.objects.filter(user=self.user).first()
            # if phone:
                # self.phone = phone.phone
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()                             
        self.user.last_name = self.nom
        self.user.first_name = self.prenom
        self.user.save()
        return super(Profil, self).save(*args, **kwargs)        


class Partie(models.Model):

    code = models.CharField(max_length=25, unique=True, editable=False)
    
    nombre_participants = models.PositiveIntegerField('nombre participants')
    montant_mise = models.DecimalField('montant mise', max_digits=10, decimal_places=2, null=True, blank=True)
    montant_cagnotte = models.DecimalField('montant cagnotte', max_digits=10, decimal_places=2, null=True, blank=True)
    montant_commission = models.DecimalField('montant commission', max_digits=10, decimal_places=2, null=True, blank=True)

    visibilite = models.CharField(max_length=20, choices=Visibilite, default=Visibilite.Public, null=True, blank=True, verbose_name = "visibilité")

    delai_tour = models.PositiveIntegerField('délai tour par joueur (sec)', null=True, blank=True)
    
    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)

    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.DateTimeField('état suppression', default=False, null=True, blank=True)

    date_demarrage = models.DateTimeField('date démarrage', null=True, blank=True)
    date_fin = models.DateTimeField('date fin', null=True, blank=True)
    
    etat_demarrage = models.BooleanField('état démarrage', default=False)
    etat_fin = models.DateTimeField('état fin', default=False, null=True, blank=True)

    mise = models.ForeignKey(Mise, models.SET_NULL, null=True, blank=True, related_name='mise_parties', related_query_name="mise_partie", verbose_name = "mise")
    taux_comission = models.ForeignKey(TauxCommission, models.SET_NULL, null=True, blank=True, related_name='taux_comission_parties', related_query_name="taux_comission_partie", verbose_name = "taux de comission")
    config = models.ForeignKey(Config, models.SET_NULL, null=True, blank=True, related_name='config_parties', related_query_name="config_partie", verbose_name = "configuration")
    organise_par = models.ForeignKey(Profil, models.SET_NULL, null=True, blank=True, related_name='organise_par_parties', related_query_name="organise_par_partie", verbose_name = "organisé par")
    vainqueur = models.ForeignKey(Profil, models.SET_NULL, null=True, blank=True, related_name='vainqueur_parties', related_query_name="vainqueur_partie", verbose_name = "vainqueur")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "partie"  
    
    def __str__(self):
        return ("{} - Mise : {} - Participants : {} - Cagnotte : {}".format(self.code, self.montant_mise, self.nombre_participants, self.montant_cagnotte))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.code = timezone.now().strftime('%d%m%Y%H%M%S%f')
            # self.email = self.user.email
            # phone = PhoneNumber.objects.filter(user=self.user).first()
            # if phone:
                # self.phone = phone.phone
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()                             
        return super(Partie, self).save(*args, **kwargs)        


class Participation(models.Model):

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)

    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.DateTimeField('état suppression', default=False, null=True, blank=True)

    date_demarrage = models.DateTimeField('date démarrage', null=True, blank=True)
    date_fin = models.DateTimeField('date fin', null=True, blank=True)
    
    etat_demarrage = models.BooleanField('état démarrage', default=False)
    etat_fin = models.DateTimeField('état fin', default=False, null=True, blank=True)

    etat_exclusion = models.BooleanField('état exclusion', default=False)
    etat_victoire = models.DateTimeField('état victoire', default=False, null=True, blank=True)

    partie = models.ForeignKey(Partie, models.SET_NULL, null=True, blank=True, related_name='partie_participations', related_query_name="partie_participation", verbose_name = "partie")
    profil = models.ForeignKey(Profil, models.SET_NULL, null=True, blank=True, related_name='profil_participations', related_query_name="profil_participation", verbose_name = "profil")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "participation"  
    
    def __str__(self):
        return ("Participation : {} - Partie : {}".format(self.profil, self.partie))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            pass
            # self.code = timezone.now().strftime('%d%m%Y%H%M%S%f')
            # self.email = self.user.email
            # phone = PhoneNumber.objects.filter(user=self.user).first()
            # if phone:
                # self.phone = phone.phone
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()                             
        return super(Participation, self).save(*args, **kwargs)        


class Transaction(models.Model):

    code = models.CharField(max_length=25, unique=True, editable=False)
    
    type = models.CharField(max_length=20, choices=TypeTransaction, null=True, blank=True, verbose_name = "type transaction")

    montant = models.DecimalField('montant', max_digits=10, decimal_places=2, null=True, blank=True)
    frais_genere = models.DecimalField('frais généré', max_digits=10, decimal_places=2, null=True, blank=True)
    
    depot = models.DecimalField('montant dépôt', max_digits=10, decimal_places=2, null=True, blank=True)
    retrait = models.DecimalField('montant retrait', max_digits=10, decimal_places=2, null=True, blank=True)
    mise = models.DecimalField('montant mise', max_digits=10, decimal_places=2, null=True, blank=True)
    gain = models.DecimalField('montant gain', max_digits=10, decimal_places=2, null=True, blank=True)

    description = models.CharField(max_length=225, unique=True, editable=False)
    
    contact_transaction = models.CharField('contact transaction', max_length=225, unique=True, editable=False)
    operateur = models.CharField('opérateur', max_length=225, unique=True, editable=False)
    type_api = models.CharField('type API', max_length=225, unique=True, editable=False)

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)

    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.DateTimeField('état suppression', default=False, null=True, blank=True)
    
    taux_frais_genere = models.ForeignKey(TauxTransaction, models.SET_NULL, null=True, blank=True, related_name='taux_frais_transactions', related_query_name="taux_frais_transaction", verbose_name = "taux de frais")
    config = models.ForeignKey(Config, models.SET_NULL, null=True, blank=True, related_name='config_transactions', related_query_name="config_transaction", verbose_name = "configuration")
    partie = models.ForeignKey(Partie, models.SET_NULL, null=True, blank=True, related_name='partie_transactions', related_query_name="partie_transaction", verbose_name = "partie")
    profil = models.ForeignKey(Profil, models.SET_NULL, null=True, blank=True, related_name='profil_transactions', related_query_name="profil_transaction", verbose_name = "profil")
    valide_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='valide_transactions', related_query_name="valide_transaction", verbose_name = "validée par")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "transaction"  
    
    def __str__(self):
        return ("{} - {} : {} - Profil : {}".format(self.code, self.type, self.montant, self.profil))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.code = timezone.now().strftime('%d%m%Y%H%M%S%f')
            # self.email = self.user.email
            # phone = PhoneNumber.objects.filter(user=self.user).first()
            # if phone:
                # self.phone = phone.phone
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()                             
        return super(Transaction, self).save(*args, **kwargs)        


class Observation(models.Model):

    observation = HTMLField("observation", unique=True, editable=False)
    
    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)

    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.DateTimeField('état suppression', default=False, null=True, blank=True)
    
    transaction = models.ForeignKey(Transaction, models.SET_NULL, null=True, blank=True, related_name='transaction_observations', related_query_name="transaction_observation", verbose_name = "transaction")
    participation = models.ForeignKey(Participation, models.SET_NULL, null=True, blank=True, related_name='participation_observations', related_query_name="participation_observation", verbose_name = "participation")
    partie = models.ForeignKey(Partie, models.SET_NULL, null=True, blank=True, related_name='partie_observations', related_query_name="partie_observation", verbose_name = "partie")
    profil = models.ForeignKey(Profil, models.SET_NULL, null=True, blank=True, related_name='profil_observations', related_query_name="profil_observation", verbose_name = "profil")
    modifie_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='modifie_observations', related_query_name="modifie_observation", verbose_name = "modifiée par")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "observation"  
    
    def __str__(self):
        complement = ""
        if self.transaction:
            complement = self.transaction
        if self.participation:
            complement = self.participation
        if self.partie:
            complement = self.partie
        if self.profil:
            complement = self.profil
        return ("{} - {}".format(complement, self.observation))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            pass
            # self.code = timezone.now().strftime('%d%m%Y%H%M%S%f')
            # self.email = self.user.email
            # phone = PhoneNumber.objects.filter(user=self.user).first()
            # if phone:
                # self.phone = phone.phone
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()                             
        return super(Observation, self).save(*args, **kwargs)        


class HistoriqueNotification(models.Model):
   
    objet = models.CharField('objet', max_length=255, null=True, blank=True)
    message = HTMLField("message", unique=True, editable=False)
    
    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)

    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.DateTimeField('état suppression', default=False, null=True, blank=True)
    
    profil = models.ForeignKey(Profil, models.SET_NULL, null=True, blank=True, related_name='profil_historique_notifications', related_query_name="profil_historique_notification", verbose_name = "profil")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "historique notification"  
    
    def __str__(self):
        return ("{} - {}".format(self.profil, self.objet))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            pass
            #self.code = timezone.now().strftime('%d%m%Y%H%M%S%f')
            # self.email = self.user.email
            # phone = PhoneNumber.objects.filter(user=self.user).first()
            # if phone:
                # self.phone = phone.phone
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()                             
        return super(HistoriqueNotification, self).save(*args, **kwargs)        




def code_generator(length): # define the function and pass the length as argument  
    # Print the string in Lowercase  
    result = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) # run loop until the define length  
    print(" Random string generated in Lowercase: ", result)  
  
    # Print the string in Uppercase  
    result1 = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) # run the loop until the define length  
    print(" Random string generated in Uppercase: ", result1)  
  
code_generator(10) # define the length  