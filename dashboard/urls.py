from django.urls import path
from .views import (
    dashboardHome,
    ClientView,client_list,
    add_client,edit_client,delete_client,
    CategoryVehiculeView,category_vehicule_list,add_category_vehicule,
    edit_category_vehicule,delete_category_vehicule,
    TarifView,tarif_list,add_tarif,edit_tarif,delete_tarif,
    VehiculeView,vehicule_list,add_vehicule,edit_vehicule,delete_vehicule,
    LocationView,location_list,add_location,edit_location,delete_location,get_tarif_by_vehicule)


urlpatterns = [
    path('dashboard',dashboardHome, name="dashboard"),
    #Client urlpattern
    path('dashboard/client_list', client_list, name='client_list'),
    path('dashboard/client',ClientView.as_view(), name="client"),
    path('dashboard/client/add_client',add_client, name="add_client"),
    path('dashboard/client/<int:pk>/edit', edit_client, name='edit_client'),
    path('dashboard/client/<int:pk>/delete', delete_client, name='delete_client'),
    
    #Category urlpattern
    path('dashboard/category_vehicule_list', category_vehicule_list, name='category_vehicule_list'),
    path('dashboard/category_vehicule',CategoryVehiculeView.as_view(), name="category_vehicule"),
    path('dashboard/category_vehicule/add_category_vehicule',add_category_vehicule, name="add_category_vehicule"),
    path('dashboard/category_vehicule/<int:pk>/edit', edit_category_vehicule, name='edit_category_vehicule'),
    path('dashboard/category_vehicule/<int:pk>/delete', delete_category_vehicule, name='delete_category_vehicule'),
    
    #Tarif urlpattern
    path('dashboard/tarif_list', tarif_list, name='tarif_list'),
    path('dashboard/load_vehicule_tarif', get_tarif_by_vehicule, name='load_vehicule_tarif'),
    path('dashboard/tarif',TarifView.as_view(), name="tarif"),
    path('dashboard/tarif/add_tarif',add_tarif, name="add_tarif"),
    path('dashboard/tarif/<int:pk>/edit',edit_tarif, name='edit_tarif'),
    path('dashboard/tarif/<int:pk>/delete', delete_tarif, name='delete_tarif'),
    
     #Vehicule urlpattern
    path('dashboard/vehicule_list', vehicule_list, name='vehicule_list'),
    path('dashboard/vehicule',VehiculeView.as_view(), name="vehicule"),
    path('dashboard/vehicule/add_vehicule',add_vehicule, name="add_vehicule"),
    path('dashboard/vehicule/<int:pk>/edit',edit_vehicule, name='edit_vehicule'),
    path('dashboard/vehicule/<int:pk>/delete', delete_vehicule, name='delete_vehicule'),
    
    #Location urlpattern
    path('dashboard/location_list', location_list, name='location_list'),
    path('dashboard/location',LocationView.as_view(), name="location"),
    path('dashboard/location/add_location',add_location, name="add_location"),
    path('dashboard/location/<int:pk>/edit',edit_location, name='edit_location'),
    path('dashboard/location/<int:pk>/delete', delete_location, name='delete_location'),

]
