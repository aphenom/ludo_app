from django.forms import EmailInput, ModelForm, TextInput, DateInput, Select, NumberInput, ClearableFileInput, Textarea, CheckboxInput
from django import forms
from player.models import Profil
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

'''formulaire pour remplir informations avant et servant pour la validation'''
class ProfilForm(forms.ModelForm):

    contact = PhoneNumberField(
        widget=TextInput(
            attrs={"class": "", "placeholder": "+2250000000000"},
            )
    )
        
    class Meta:
        model = Profil
        exclude = ['code', 'id_facebook', 'contact_retrait', 'photo', 'pays_residence', 'user', 'modifie_par', 'invite_par', 'etat_validation', 'etat_suppression', 'date_suppression', 'date_validation', 'date_modification', 'date_creation']
        
        fields = ['nom', 'prenom', 'genre', 'contact', 'email', 'code_invite_par']
        
        widgets = {
            'nom': TextInput(attrs={'placeholder':'Ton nom de famille (officiel)'}),
            'prenom': TextInput(attrs={'placeholder':'Tes prénoms (officiels)', 'class':''}),
            'code_invite_par': TextInput(attrs={'placeholder':'Le code de la personne qui t\' invité', 'class':''}),
            'genre': Select(attrs={'class':''}),
            # 'pays_residence': Select(attrs={'class':'form-control select2', 'data-select' : 'true'}),
            'email': EmailInput(attrs={'placeholder':"Ton adresse mail", 'class':''}),
            # "contact": PhoneNumberPrefixWidget(
            #     attrs={"class": "p2 col-md-6 col-12", "placeholder": "0000000000"},
            # ),
        }

