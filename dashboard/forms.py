from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from AutoHeavenWebsite.models import User,CategoryVehicule,Tarif,Vehicule,Location


class ClientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','nom','prenom','sexe','numero_de_telephone','addresse','password')
        widgets = {
           'username':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":"",
                
            }
        
        ),
           
           'nom':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
            
           'prenom':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
            'sexe':forms.Select(
            attrs={
                "class": "form-control shadow-none",
            }
        ),
           'numero_de_telephone':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
           'addresse':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
           'password':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "type":"password",
                "value":""
                
            }
        ),
        }

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nom','prenom','sexe','numero_de_telephone','addresse')
        widgets = {
            'nom':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
           'prenom':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
            'sexe':forms.Select(
            attrs={
                "class": "form-control shadow-none",
            }
        ),
           'numero_de_telephone':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
           'addresse':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
        }
class CategoryVehiculeForm(forms.ModelForm):
    class Meta:
        model = CategoryVehicule
        fields = ('libelle','description')
        widgets = {
            
           'libelle':forms.TextInput(
            attrs={
                "class": "form-control shadow-none",
                "value":""
                
            }
        ),
           'description':forms.Textarea(
            attrs={
                "class": "form-control shadow-none",
                "maxlength":"600",
                "rows":"4",
                "cols":"50"
                
            }
        )
        }
        
class TarifForm(forms.ModelForm):
    class Meta:
        model = Tarif
        fields = ('category_vehicule','prix','periodicite')
        widgets = {
           'category_vehicule':forms.Select(
            attrs={
                "class": "form-control shadow-none",
            }
        ),
           'prix':forms.TextInput(   
            attrs={
                "class": "form-control shadow-none",
                "type":"number"
            }),
            'periodicite':forms.Select(
            attrs={
                "class": "form-control shadow-none",
            }
        ),
        
        }
class VehiculeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proprio_vehicule'].queryset = User.objects.filter(role='Proprio')
    class Meta:
        model = Vehicule
        fields = ('category_vehicule','immatriculation','marque','model','statut','image','proprio_vehicule')
        widgets = {
           'category_vehicule':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":""
            }
        ),
           'immatriculation':forms.TextInput(   
            attrs={
                "class": "form-control shadow-none",
                "type":"text",
                "value":""
            }),
           'marque':forms.TextInput(   
            attrs={
                "class": "form-control shadow-none",
                "type":"text",
                "value":""
            }),
           'model':forms.TextInput(   
            attrs={
                "class": "form-control shadow-none",
                "type":"text",
                "value":""
            }),
           'statut':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":""
            }
        ),
           'proprio_vehicule':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":""
            }
        ),
            'image':forms.FileInput(
            attrs={
                "class": "form-control shadow-none",
                "type":"file",
                "accept":".png,.jpeg,.jpg,.webp"
            }
        ),
        
        }
class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = User.objects.filter(role='Client')

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
        fields = ('vehicule','client','date_debut','date_fin','statut','tarif')
        widgets = {
           'vehicule':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":"",
                "id": "vehicule_id",
                "name":"vehicule",
                "hx-get":"load_vehicule_tarif",
                "hx-target":"#id_tarif"
            }
        ),
           'client':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":""
            }
        ),
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
           
           'statut':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":""
            }
        ),
            'tarif':forms.Select(
            attrs={
                "class": "form-control shadow-none",
                "value":"",
                "name":"tarif",
                "id":"id_tarif"
            }
        ),
        
        }

