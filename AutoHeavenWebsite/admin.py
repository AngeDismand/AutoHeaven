from django.contrib import admin
from .models import User,CategoryVehicule,Tarif,Vehicule,Location

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','username','is_active','is_staff')


admin.site.register(CategoryVehicule)
admin.site.register(Tarif)
admin.site.register(Vehicule)
admin.site.register(Location)

