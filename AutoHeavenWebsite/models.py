import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.
def vehicule_directory_path(instance, filename):
    return os.path.join("vehicule_image", instance.immatriculation, filename)
class Verification :
    Sexe = {
        'M' : 'Masculin',
        'F' : 'Féminin'
    
    }
    Role = {
        'Employé':'Employé',
        'Client':'Client',
        'Proprio':'Proprio',
        'SuperAdmin':'SuperAdmin'
    }
    Statut = {
        'Disponible':'Disponible',
        'Occupé':'Occupé',
        'En attente':'En attente'
    }
    StatutPaiement = {
        'Payé':'Payé',
        'En attente':'En attente'
    }
    Periodicite = {
        'Journalier':'Journalier',
        'Hebdomadaire':'Hebdomadaire',
        'Mensuel':'Mensuel',
        'Annuelle':'Annuelle'
    }
    

class User(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField( null=True, default="1980-01-01",verbose_name='date de naissance')
    sexe = models.CharField(max_length=10, choices=Verification.Sexe)
    addresse = models.CharField(max_length=100)
    numero_de_telephone = models.CharField(max_length=20)
    role=models.CharField(max_length=10, choices=Verification.Role)
    
    def __str__(self):
        return f'{self.username}'
   
class CategoryVehicule(models.Model):
    libelle = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=600)
    def __str__(self):
        return f'{self.libelle}'
    
class Tarif(models.Model):
    uniq_tarif=  models.CharField(max_length=100,null=True,unique=True)
    category_vehicule = models.ForeignKey(CategoryVehicule,  on_delete=models.CASCADE)
    prix = models.IntegerField(validators=[MinValueValidator(0)])
    periodicite = models.CharField(max_length=12, choices=Verification.Periodicite)
    def __str__(self):
        return f'{self.category_vehicule}, {self.periodicite}/{self.prix}'

class Vehicule(models.Model):
    category_vehicule = models.ForeignKey(CategoryVehicule,  on_delete=models.CASCADE)
    proprio_vehicule = models.ForeignKey(User,  null=True, on_delete=models.CASCADE)
    tarif_ids =  models.ManyToManyField(Tarif,verbose_name='Liste des tarifs')
    immatriculation =  models.CharField(max_length=100, unique=True)
    marque = models.CharField(max_length=15)
    model = models.CharField(max_length=15)
    statut= models.CharField(max_length=12, choices=Verification.Statut)
    image = models.FileField(upload_to=vehicule_directory_path, blank=True, null=True)
    def __str__(self):
        return f'{self.immatriculation} - {self.marque} - {self.model}'
    

    
class Location(models.Model):
    vehicule = models.ForeignKey(Vehicule,  on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    tarif = models.ForeignKey(Tarif,null=True, on_delete=models.CASCADE)
    location_libelle = models.CharField(max_length=500)
    date_debut = models.DateField(verbose_name='date de début')
    date_fin =  models.DateField(verbose_name='date de fin')
    montant_total = models.IntegerField(validators=[MinValueValidator(0)])
    statut= models.CharField(max_length=12, choices=Verification.StatutPaiement)
    def __str__(self):
        return f'{self.location_libelle}'