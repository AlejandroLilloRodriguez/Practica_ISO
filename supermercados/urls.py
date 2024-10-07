# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('supermercados/', views.supermercados, name='supermercados'),  # Ruta para iniciar sesión y registrarse
]