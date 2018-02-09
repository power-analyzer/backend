from django.urls import path

from . import views

app_name = 'datapoints'
urlpatterns = [
    path('', views.index, name='index'),
    path('request/', views.register_device, name="register"),
    path('<int:device_id>/batch/', views.batch_upload, name="batch_upload"),
    path('<int:device_id>/<int:circuit_id>/', views.upload, name="upload"),
]
