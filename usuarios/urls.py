# usuarios/urls.py
from django.urls import path
from . import views
from .views import reset_password
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),  # Ruta para iniciar sesión y registrarse
    path('perfil/', views.editar_perfil, name='perfil'),  # Ruta para ver el perfil del usuario
   
    path('reset-password/', reset_password, name='reset_password'),  # Ruta para restablecer la contraseña
        path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Define la URL para el inicio de sesión

]

