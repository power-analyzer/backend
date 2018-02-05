from django.urls import path

from . import views

app_name = 'datapoints'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:device_id>/<int:circuit_id>/', views.upload, name="upload")
]
