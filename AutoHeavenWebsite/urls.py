from django.urls import path
from .views import (
    home, 
    login_view,register_view,LogoutView,reservation_list,reservation,add_reservation,vehicule_disponible)


urlpatterns = [
    path('',home, name="home"),
    path('login/', login_view, name="login"),
    path('register/',register_view, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    ####Reservation
    path('reservation/reservation_list', reservation_list, name='reservation_list'),
    path('reservation/vehicule_disponible', vehicule_disponible, name='vehicule_disponible'),
    path('reservation/mes_reservations',reservation, name="mes_reservations"),
    path('reservation/<int:pk>/<int:tarif_id>/add_reservation',add_reservation, name="add_reservation"),
   

]
