# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),  # Ruta para iniciar sesión y registrarse
]