from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Define las urls del sitio web

urlpatterns = [
  path('', views.Home, name="home"), # Url de la pagina principal
]