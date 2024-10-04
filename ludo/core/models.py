from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from ludo.enum import TypeTransaction

# Create your models here.
class TauxTransaction(models.Model):

    type = models.CharField(max_length=20, choices=TypeTransaction.choices, null=True, blank=True, verbose_name = "type transaction")
    taux = models.DecimalField('taux', max_digits=10, decimal_places=2, null=True, blank=True)
    debut = models.DateTimeField('date début')
    fin = models.DateTimeField('date fin', null=True, blank=True)

    observation = models.TextField('observation', null=True, blank=True)

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)
    
    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.BooleanField('état suppression', default=False)
    
    modifie_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='modifie_taux_transactions', related_query_name="modifie_taux_transaction", verbose_name = "modifié par")
   
    class Meta:
        ordering = ['-debut']
        verbose_name = "taux transaction"  
        
    def __str__(self):
        return self.taux

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()   
        return super(TauxTransaction, self).save(*args, **kwargs)        


class TauxCommission(models.Model):

    taux = models.DecimalField('taux', max_digits=10, decimal_places=2, null=True, blank=True)
    debut = models.DateTimeField('date début')
    fin = models.DateTimeField('date fin', null=True, blank=True)

    observation = models.TextField('observation', null=True, blank=True)

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)
    
    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.BooleanField('état suppression', default=False)
    
    modifie_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='modifie_taux_commissions', related_query_name="modifie_taux_commission", verbose_name = "modifié par")
   
    class Meta:
        ordering = ['-debut']
        verbose_name = "taux commission"  
        
    def __str__(self):
        return self.taux

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()   
        return super(TauxCommission, self).save(*args, **kwargs)        


class Mise(models.Model):

    montant = models.DecimalField('montant', max_digits=10, decimal_places=2, null=True, blank=True)
    nombre_minimum = models.PositiveIntegerField('nombre minimum participants', null=True, blank=True)

    observation = models.TextField('observation', null=True, blank=True)

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)
    
    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.BooleanField('état suppression', default=False)
    
    modifie_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='modifie_mises', related_query_name="modifie_mise", verbose_name = "modifié par")
   
    class Meta:
        ordering = ['-montant', '-date_creation']
        verbose_name = "mise"  
        
    def __str__(self):
        return self.montant

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()   
        return super(TauxCommission, self).save(*args, **kwargs)        


class Config(models.Model):
    ''' Stock la configuration générale de la plateforme '''
    app_name = models.CharField('nom plateforme', max_length=50)
    slogan = models.CharField("slogan", max_length=100, null=True, blank=True)
    email = models.EmailField("email", max_length=100, null=True, blank=True)
    currency = models.CharField("monnaie", max_length=15, null=True, blank=True)
    contact = models.CharField("contact", max_length=100, null=True, blank=True)
    address = models.CharField("adresse", max_length=100, null=True, blank=True)
    sms_api_url = models.CharField("SMS Base URL", max_length=100, null=True, blank=True)
    sms_api_id = models.CharField("SMS API ID", max_length=100, null=True, blank=True)
    sms_api_key = models.CharField("SMS API KEY", max_length=100, null=True, blank=True)
    notification_api_url = models.CharField("Notification Base URL", max_length=100, null=True, blank=True)
    notification_api_id = models.CharField("Notification API ID", max_length=100, null=True, blank=True)
    notification_api_key = models.CharField("Notification API KEY", max_length=100, null=True, blank=True)
    notification_api_url = models.CharField("Notification Base URL", max_length=100, null=True, blank=True)
    sms_api_id = models.CharField("SMS API ID", max_length=100, null=True, blank=True)
    sms_api_key = models.CharField("SMS API KEY", max_length=100, null=True, blank=True)
    email_api_url = models.CharField("Email Base URL", max_length=100, null=True, blank=True)
    email_api_id = models.CharField("Email API ID", max_length=100, null=True, blank=True)
    email_api_key = models.CharField("Email API KEY", max_length=100, null=True, blank=True)
    transaction_api_url = models.CharField("Paiement Base URL", max_length=100, null=True, blank=True)
    transaction_api_id = models.CharField("Paiement API ID", max_length=100, null=True, blank=True)
    transaction_api_key = models.CharField("Paiement API KEY", max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='uploaded_media/config/logos')
    logo_symbol = models.ImageField(upload_to='uploaded_media/config/logo_symbols')
    favicon = models.ImageField(upload_to='uploaded_media/config/favicons')
    minimum_retrait = models.DecimalField('montant minimum de retrait', max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_depot = models.DecimalField('montant minimum de dépôt', max_digits=10, decimal_places=2, null=True, blank=True)
    note_information = HTMLField("note d'information", null=True, blank=True)
    faq = HTMLField("faq", null=True, blank=True)
    about = HTMLField("a propos", null=True, blank=True)
    privacy_policy = HTMLField("politique de confidentialité", null=True, blank=True)
    condition_term = HTMLField("Conditions d'utilisation", null=True, blank=True)

    delai_tour = models.PositiveIntegerField('délai tour (sec)', null=True, blank=True)
    
    etat_retrait = models.BooleanField('état retrait', default=True)
    etat_validation_prealable_retrait = models.BooleanField('état validation prealable retrait', default=True)
    etat_depot = models.BooleanField('état dépôt', default=True)
    etat_partie = models.BooleanField('état partie', default=True)

    date_creation = models.DateTimeField('date création', auto_now_add=True)
    date_modification = models.DateTimeField('date modification', null=True, blank=True, auto_now=True)
    date_validation  = models.DateTimeField('date validation', null=True, blank=True)
    date_suppression = models.DateTimeField('date suppression', null=True, blank=True)
    
    etat_validation = models.BooleanField('état validation', default=True)
    etat_suppression = models.BooleanField('état suppression', default=False)
    
    modifie_par = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name='modifie_configs', related_query_name="modifie_config", verbose_name = "modifié par")

   
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "config"  

    def __str__(self):
        return self.app_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_etat_validation = self.etat_validation
        self._init_etat_suppression = self.etat_suppression

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.etat_validation != self._init_etat_validation:
            if self.etat_validation == True:
                self.date_validation = timezone.now()
        if self.etat_suppression != self._init_etat_suppression:
            if self.etat_suppression == True:
                self.date_suppression = timezone.now()   
        return super(Config, self).save(*args, **kwargs)        

