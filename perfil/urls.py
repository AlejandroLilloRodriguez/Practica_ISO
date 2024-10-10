from django.urls import path
from .views import perfil

from .views import reset_password

urlpatterns = [
    path('', perfil, name='perfil'),  # Ruta para la vista de perfil
        path('reset-password/', reset_password, name='reset_password'),  # Añade esta línea

]
