from django.contrib import admin

from .models import Building, Device, Circuit, Measurement, UnarchivedMeasurement, Alert

admin.site.register(Building)
admin.site.register(Device)
admin.site.register(Circuit)
admin.site.register(Measurement)
admin.site.register(UnarchivedMeasurement)
admin.site.register(Alert)
