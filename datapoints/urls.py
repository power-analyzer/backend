from django.urls import path

from . import views

app_name = 'datapoints'
urlpatterns = [
    path('', views.index, name='index'),
]
