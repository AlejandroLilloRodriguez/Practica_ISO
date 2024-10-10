# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),  # Ruta para iniciar sesión y registrarse
    path('perfil/', views.editar_perfil, name='perfil'),  # Ruta para ver el perfil del usuario
]