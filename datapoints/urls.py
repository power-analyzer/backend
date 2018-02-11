from django.urls import path

from . import views

app_name = 'datapoints'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/<str:mac>', views.register_device, name="register"),
    path('<str:mac>/batch/', views.batch_upload, name="batch_upload"),
]
