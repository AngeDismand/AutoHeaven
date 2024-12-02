from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import LoginForm,RegisterForm
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views import View
from .models import Vehicule,Tarif,Location,User
from dashboard.views import rechercher_tarif_par_id,calculer_montant_total
from .forms import ReservationForm
import random
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
# Create your views here.
def home(request):
    vehicules = Vehicule.objects.all()
    vehicule_infos = []
    for vehicule in vehicules:
        #tarif= Tarif.objects.get(category_vehicule=vehicule.category_vehicule)
        vehicule_info = {
            'vehicule': vehicule,
            #'tarif': tarif,
        }
        vehicule_infos.append(vehicule_info)


    context = {'user': request.user,
               'vehicule_infos': vehicule_infos
               
               }
    return render(request, 'home/home.html',context)
################ Reservation ################################
@login_required  
def add_reservation(request, pk,tarif_id):
    msg = None
    vehicule = get_object_or_404(Vehicule, pk=pk)
    form = ReservationForm(request.POST or None)
    msg = None
    if(vehicule.statut ==  'Disponible'):
        
        if request.method == "POST":
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.client = request.user
                tarifInformation = rechercher_tarif_par_id(tarif_id)
                reservation.tarif = tarifInformation
                reservation.vehicule = vehicule
                reservation.statut = 'En attente'
                reservation.location_libelle = str(reservation.vehicule) + str(reservation.client) +str(random.randint(100, 999))
                reservation.montant_total = calculer_montant_total(str(reservation.date_debut), str(reservation.date_fin),tarifInformation.periodicite,tarifInformation.prix)
                vehicule.statut = 'Occupé'
                vehicule.save()
                reservation.save()
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "movieListChanged": None,
                            "showMessage":"La réservation a été mise en attente"
                        })
                    }
                )
            
            else:
                msg="La date de début ou de fin ne peut pas être dans le passé"
        return render(request, "reservation/reservation_form.html", {"form": form, "msg": msg})
    else:
        msg="Le véhicule n'est plus disponible, vous nous envoyez désolé."
    return render(request, "reservation/reservation_form.html", {"form": form, "msg": msg})
@login_required 
def reservation_list(request):
    utilisateur_connecte = request.user
    reservations = Location.objects.filter(client=utilisateur_connecte)
    reservation_infos = []
    for reservation in reservations:
        reservation_info = {
            'vehicule': reservation.vehicule,
            'tarif': reservation.tarif,
            'reservation':reservation
        }
        reservation_infos.append(reservation_info)
    context = {'user': request.user,
               'reservations':reservation_infos
               
               }
    return render(request, 'reservation/reservation_list.html', context)
@login_required
def reservation(request):
    context = {'user': request.user}
    return render(request, 'reservation/reservation.html', context)
@login_required
def vehicule_disponible(request):
    vehicules = Vehicule.objects.filter(statut='Disponible')
    vehicule_infos = []
    tarifs = []
    for vehicule in vehicules:
        if(vehicule.tarif_ids):
            vehicule_tarifs= vehicule.tarif_ids.all()
            for one_tarif in vehicule_tarifs:
                tarifs.append(one_tarif)
        vehicule_info = {
            'vehicule': vehicule,
            'tarifs': tarifs,
        }
        vehicule_infos.append(vehicule_info)
        tarifs = []
    utilisateur_connecte = request.user
    reservations = Location.objects.filter(client=utilisateur_connecte)
    context = {'user': request.user,
               'vehicule_infos': vehicule_infos,
               'reservations':reservations
               
               }
    return render(request, 'reservation/vehicule_disponible.html', context)

def register_view(request):
    form = RegisterForm(request.POST or None)
    msg = None
    status = True
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            sexe = form.cleaned_data['sexe']
            email = form.cleaned_data['email']
            role="Client"
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, nom=nom,prenom=prenom,sexe=sexe,email=email,
                                            role=role,password=password)
            msg = "Votre compte client a été créé avec succès😎, veuillez-vous connectez, en remplissant le formulaire ci-dessous"
            request.session['inscription_message'] = msg
            request.session['inscription_status'] = status
            return redirect("/login")
           
           
        else:
            msg="L'utilisateur avec ce même nom d'utilisateur existe déjà"
    return render(request, "register.html", {"form": form, "msg": msg})
    
    
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = request.session.pop('inscription_message', None)
    status = request.session.pop('inscription_status', None)
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if(request.user.role=='Client'):
                    return redirect("/reservation/mes_reservations")
                elif(request.user.role=='Employé' or request.user.is_superuser):
                    
                    return redirect("/dashboard")
            else:
                msg = 'Nom d\'utilisateur ou mot de passe incorrect'
        else:
            msg = 'Erreur'

    return render(request, "login.html", {"form": form, "msg": msg,"status":status})
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login') 