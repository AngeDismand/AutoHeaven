import json
import random
import os
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from functools import wraps
from AutoHeavenWebsite.models import User,CategoryVehicule,Tarif,Vehicule,Location
from .forms import ClientForm,ClientUpdateForm,CategoryVehiculeForm,TarifForm,VehiculeForm,LocationForm
# Create your views here.

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def is_employee(user):
    return user.is_authenticated and user.role == 'Employé'
def user_is_employee_or_superuser(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'Employé'):
            return function(request, *args, **kwargs)
        else:
           return redirect('login') 
    return wrapper

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u))  
def dashboardHome(request):    
    return render(request, 'home_dashboard.html',{})

#client crud#############################
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def client_list(request):
    return render(request, 'client/client_list.html', {
        'clients': User.objects.all(),
    })
    
@method_decorator(user_is_employee_or_superuser, name='dispatch')
class ClientView(ListView):
    model = User
    template_name = 'client/client.html'
    

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def add_client(request):
    form = ClientForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            sexe = form.cleaned_data['sexe']
            numero_de_telephone = form.cleaned_data['numero_de_telephone']
            addresse = form.cleaned_data['addresse']
            role="Proprio"
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, nom=nom,prenom=prenom,sexe=sexe,numero_de_telephone=numero_de_telephone,
                                            addresse=addresse,role=role,password=password)
            return HttpResponse(
                status=204,
                headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": "Client ajouté avec succès."
                })
            }
        )
        else:
            msg="L'utilisateur avec ce même nom d'utilisateur existe déjà"
    return render(request, "client/client_form.html", {"form": form, "msg": msg})
    
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u))  
def edit_client(request, pk):
    client = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ClientUpdateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage":f"{client.username} modifié avec succès."
                    })
                }
            )
    else:
        form = ClientUpdateForm(instance=client)
    return render(request, 'client/client_update_form.html', {
        'form': form,
        'client': client,
    })
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def delete_client(request, pk):
    client = get_object_or_404(User, pk=pk)
    client.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": "Le client a été supprimé avec succès."
            })
        })

###########CategoryVehicule ################"###########################################################################################################################

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def category_vehicule_list(request):
    return render(request, 'category_vehicule/category_vehicule_list.html', {
        'categories': CategoryVehicule.objects.all(),
    })
    
@method_decorator(user_is_employee_or_superuser, name='dispatch')
class CategoryVehiculeView(ListView):
    model = CategoryVehicule
    template_name = 'category_vehicule/category_vehicule.html'
    

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def add_category_vehicule(request):
    form = CategoryVehiculeForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.libelle = category.libelle.upper()
                category.save()
                return HttpResponse(
                    status=204,
                    headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": "Catégorie de voiture ajouté avec succès."
                    })
                }
            )
            except :
                msg="La catégorie existe déjà"
                return render(request, "category_vehicule/category_vehicule_form.html", {"form": form, "msg": msg})
            
        else:
            msg="La catégorie existe déjà"
    return render(request, "category_vehicule/category_vehicule_form.html", {"form": form, "msg": msg})


   
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u))  
def edit_category_vehicule(request, pk):
    category_vehicule = get_object_or_404(CategoryVehicule, pk=pk)
    if request.method == "POST":
        form = CategoryVehiculeForm(request.POST, instance=category_vehicule)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.libelle = category.libelle.upper()
                category.save()
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "movieListChanged": None,
                            "showMessage":"La catégorie a été modifiée avec succès"
                        })
                    }
                )
            except :
                msg="La catégorie existe déjà"
                return render(request, "category_vehicule/category_vehicule_form.html", {"form": form, "msg": msg})
            
    else:
        form = CategoryVehiculeForm(instance=category_vehicule)
    return render(request, 'category_vehicule/category_vehicule_form.html', {
        'form': form,
        'category_vehicule': category_vehicule,
    })
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def delete_category_vehicule(request, pk):
    category = get_object_or_404(CategoryVehicule, pk=pk)
    category.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": "La catégorie a été supprimée avec succès."
            })
        })

###########vehicule ################"###########################################################################################################################
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def vehicule_list(request):
    return render(request, 'vehicule/vehicule_list.html', {
        'vehicules': Vehicule.objects.all(),
    })
    
@method_decorator(user_is_employee_or_superuser, name='dispatch')
class VehiculeView(ListView):
    model = Vehicule
    template_name = 'vehicule/vehicule.html'
    

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def add_vehicule(request):
    msg = None
    form = VehiculeForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            vehicule = form.save(commit=False)
            vehicule_tarif = Tarif.objects.filter(category_vehicule=vehicule.category_vehicule)
            vehicule.save()
            if(len(vehicule_tarif) > 0) : 
                for one_tarif in vehicule_tarif:
                    vehicule.tarif_ids.add(one_tarif)
           
            return HttpResponse(
                status=204,
                headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": "Le véhicule a été enregistré avec succès."
                })
            }
        )
        else:
            msg="on a déjà un véhicule de la même immatriculation "
    return render(request, "vehicule/vehicule_form.html", {"form": form, "msg": msg})


@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u))  
def edit_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    old_image_path = "media/"+str(vehicule.image)
    if request.method == "POST":
        form = VehiculeForm(request.POST or None, request.FILES or None, instance=vehicule)
        if form.is_valid():
            new_image = os.path.basename(str(form.cleaned_data["image"]))
            old_image = os.path.basename(old_image_path)
            if os.path.isfile(old_image_path):
                if new_image and old_image != new_image:
                    os.remove(str(old_image_path))
                    
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage":"Le véhicule a été mis à jour avec succès"
                    })
                }
            )
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'vehicule/vehicule_form.html', {
        'form': form,
        'vehicule': vehicule,
    })
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def delete_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    old_image_path = "media/"+str(vehicule.image)
    if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
    vehicule.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": "Le vehicule a été retiré avec succès."
            })
        })
    
###########location ################"###########################################################################################################################

def get_tarif_by_vehicule(request):
    vehicule_id =  request.GET.get('vehicule')
    vehicule = Vehicule.objects.get(id=vehicule_id)
    tarifs = vehicule.tarif_ids.all()
    return render(request, "location/vehicule_tarif.html", {"tarifs": tarifs})
def rechercher_tarif_par_id(tarif_id):
    try:
        tarif = Tarif.objects.get(id=tarif_id)
        return tarif
    except Tarif.DoesNotExist:
        return None 

def calculer_montant_total(date_debut, date_fin, periodicite, prix):
    # Convertir les chaînes de date en objets datetime
    date_debut = datetime.strptime(str(date_debut), '%Y-%m-%d')
    date_fin = datetime.strptime(str(date_fin), '%Y-%m-%d')

    # Calculer la durée de la location en jours
    duree_location = (date_fin - date_debut).days
    if date_fin == date_debut:
        duree_location = 1
    # Calculer le montant total en fonction de la périodicité
    if periodicite == 'Journalier':
        montant_total = duree_location * prix
    elif periodicite == 'Mensuel':
        # Diviser la durée en mois et ajouter 1 si la location dépasse un mois complet
        nombre_mois = (date_fin.year - date_debut.year) * 12 + date_fin.month - date_debut.month
        if date_fin.day >= date_debut.day:
            nombre_mois += 1
        montant_total = nombre_mois * prix
    elif periodicite == 'Hebdomadaire':
        nombre_semaines = duree_location // 7
        if duree_location % 7 != 0:
            nombre_semaines += 1
        montant_total = nombre_semaines * prix
    elif periodicite == 'Annuelle':
        nombre_annees = (date_fin.year - date_debut.year)
        if date_fin.month > date_debut.month or (date_fin.month == date_debut.month and date_fin.day >= date_debut.day):
            nombre_annees += 1
        montant_total = nombre_annees * prix
    else:
        raise ValueError("Périodicité non prise en charge")

    return montant_total
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def location_list(request):
    return render(request, 'location/location_list.html', {
        'locations': Location.objects.all(),
    })
    
@method_decorator(user_is_employee_or_superuser, name='dispatch')
class LocationView(ListView):
    model = Location
    template_name = 'location/location.html'
    

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def add_location(request):
    form = LocationForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            location = form.save(commit=False)
            tarifInformation = rechercher_tarif_par_id(location.tarif.id)
            location.location_libelle = str(location.vehicule) + str(location.client) +str(random.randint(100, 999))
            location.tarif = location.tarif
            location.montant_total = calculer_montant_total(str(location.date_debut), str(location.date_fin),tarifInformation.periodicite,tarifInformation.prix)
            vehicule = Vehicule.objects.get(id = location.vehicule.id)
            vehicule.statut = 'Occupé'
            vehicule.save()
            location.save()
            return HttpResponse(
                status=204,
                headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": f"Le statut de location de véhicule est: {location.statut}"
                })
            }
        )
        else:
            msg="La date de début ou de fin ne peut pas être dans le passé"
    return render(request, "location/location_form.html", {"form": form, "msg": msg})


   
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u))  
def edit_location(request, pk):
    msg = None
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            tarifInformation = rechercher_tarif_par_category(location.vehicule.category_vehicule)
            location.montant_total = calculer_montant_total(str(location.date_debut), str(location.date_fin),tarifInformation.periodicite,tarifInformation.prix)
            location.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage":"Les données ont été modifiées avec succès"
                    })
                }
            )
        else:
            msg="La date de début ou de fin ne peut pas être dans le passé"
        return render(request, 'location/location_form.html', {
        'form': form,
        'msg': msg,
    })
           
    else:
         form = LocationForm(instance=location)
    return render(request, 'location/location_form.html', {
        'form': form,
        'msg': msg,
    })
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    vehicule = Vehicule.objects.get(id = location.vehicule.id)
    vehicule.statut = 'Disponible'
    vehicule.save()
    location.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": "Cette donnée a été retirée avec succès."
            })
        })
###########Tarif ################"###########################################################################################################################
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def tarif_list(request):
    return render(request, 'tarif/tarif_list.html', {
        'tarifs': Tarif.objects.all(),
    })
    
@method_decorator(user_is_employee_or_superuser, name='dispatch')
class TarifView(ListView):
    model = Tarif
    template_name = 'tarif/tarif.html'
    

@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def add_tarif(request):
    form = TarifForm(request.POST or None)
    msg = None
    if request.method == "POST":
       
        if form.is_valid():
            try:
                tarif  = form.save(commit=False)
                tarif.uniq_tarif = str(tarif.category_vehicule) + '_' + tarif.periodicite
                tarif = form.save()
                return HttpResponse(
                    status=204,
                    headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": "Le tarif a été ajouté avec succès."
                    })
                }
                )
            except :
                msg="Le tarif existe déjà, souhaitez vous le mettre à jour?Alors allez l'éditer"
                return render(request, "tarif/tarif_form.html", {"form": form, "msg": msg})
        else:
            msg="Une erreur c'est produite"
    return render(request, "tarif/tarif_form.html", {"form": form, "msg": msg})


   
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u))  
def edit_tarif(request, pk):
    tarif = get_object_or_404(Tarif, pk=pk)
    if request.method == "POST":
        form = TarifForm(request.POST, instance=tarif)
        if form.is_valid():
            
            try:
                tarif  = form.save(commit=False)
                tarif.uniq_tarif = str(tarif.category_vehicule) + '_' + tarif.periodicite
                tarif = form.save()
                return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage":"Le tarif a été modifié avec succès"
                    })
                }
            )
            except :
                msg="Le tarif existe déjà, souhaitez vous le mettre à jour?Alors allez l'éditer"
                return render(request, "tarif/tarif_form.html", {"form": form, "msg": msg})
    else:
        form = TarifForm(instance=tarif)
    return render(request, 'tarif/tarif_form.html', {
        'form': form,
        'tarif': tarif,
    })
@login_required  
@user_passes_test(lambda u: is_superuser(u) or is_employee(u)) 
def delete_tarif(request, pk):
    tarif = get_object_or_404(Tarif, pk=pk)
    tarif.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": "Le tarif a été supprimé avec succès."
            })
        })