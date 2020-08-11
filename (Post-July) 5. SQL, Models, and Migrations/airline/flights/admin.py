from django.contrib import admin

from .models import Airport, Flight, Passenger

# Register your models here.
# look up django documentation of admin interface

class FlightAdmin(admin.ModelAdmin):
    list_display = ("__str__", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
    

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) #Specify specific settings when viewing the admin interface
admin.site.register(Passenger, PassengerAdmin)
