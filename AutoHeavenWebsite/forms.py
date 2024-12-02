
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Location,Vehicule,User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                "class": "login__input",
                "value":" "
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "login__input",
                "value":""
            }
        ))
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','nom','prenom','sexe','password')
        widgets = {
          'username':forms.TextInput(   
            attrs={
                "class": "form-control  mr-4 shadow-none",
                "type":"text"
            }),
           'email':forms.TextInput(   
            attrs={
                "class": "form-control mr-4 shadow-none",
                "type":"email"
            }),
           'nom':forms.TextInput(   
            attrs={
                "class": "form-control  mr-4 shadow-none",
                "type":"text"
            }),
           'prenom':forms.TextInput(   
            attrs={
                "class": "form-control  mr-4 shadow-none",
                "type":"text"
            }),
            'sexe':forms.Select(
            attrs={
                "class": "form-control mr-4 shadow-none",
            }),
           'password':forms.TextInput(   
            attrs={
                "class": "form-control  mr-4 shadow-none",
                "type":"password"
            }),
           
        
        }

class ReservationForm(forms.ModelForm):
    def clean_date_debut(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        if date_debut < timezone.now().date():
            raise ValidationError("La date de début ne peut pas être dans le passé.")
        return date_debut

    def clean_date_fin(self):
        date_fin = self.cleaned_data['date_fin']
        if date_fin < timezone.now().date():
            raise ValidationError("La date de fin ne peut pas être dans le passé.")
        return date_fin
    class Meta:
        model = Location
        fields = ('date_debut','date_fin')
        widgets = {
          'date_debut':forms.TextInput(   
            attrs={
                "class": "form-control shadow-none",
                "type":"date"
            }),
           'date_fin':forms.TextInput(   
            attrs={
                "class": "form-control shadow-none",
                "type":"date"
            }),
           
        
        }

        
  