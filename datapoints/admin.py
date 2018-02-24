from django.contrib import admin

from .models import Building, Device, Circuit, Measurement, UnarchivedMeasurement

admin.site.register(Building)
admin.site.register(Device)
admin.site.register(Circuit)
admin.site.register(Measurement)
admin.site.register(UnarchivedMeasurement)
