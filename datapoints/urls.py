from django.urls import path

from datapoints.views import buildings, measurements, devices, circuits

app_name = 'datapoints'
urlpatterns = [
    path('', measurements.index, name='index'),
    path('register/<str:mac>', measurements.register_device, name="register"),
    path('<str:mac>/batch/', measurements.batch_upload, name="batch_upload"),
    path('buildings/<int:id>', buildings.get_building, name="get_buildings"),
    path('buildings', buildings.get_buildings, name="get_buildings"),
    path('devices/<int:id>', devices.get_device, name="get_device"),
    path('devices', devices.get_devices, name="get_devices"),
    path('circuits/<int:id>/<str:end_date>/<str:start_date>', circuits.get_usage),
    path('circuits/<int:id>/<str:end_date>', circuits.get_current_usage),
    path('circuits/<int:id>', circuits.get_circuit, name="get_circuit"),
    path('circuits', circuits.get_circuits, name="get_circuits"),
]
