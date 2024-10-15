from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('perfil/', views.editar_perfil, name='perfil'),
    path('reset-password/', views.password_reset_request, name='usuarios_reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),  # Agrega esta línea
]


