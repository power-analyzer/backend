from django.urls import path

from datapoints.views import buildings, measurements

app_name = 'datapoints'
urlpatterns = [
    path('', measurements.index, name='index'),
    path('register/<str:mac>', measurements.register_device, name="register"),
    path('<str:mac>/batch/', measurements.batch_upload, name="batch_upload"),
    path('buildings/<int:id>', buildings.get_building, name="get_buildings"),
    path('buildings', buildings.get_buildings, name="get_buildings"),
]
