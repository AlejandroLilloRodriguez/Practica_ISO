from django.urls import path
from .views import buscador_productos

urlpatterns = [
    path('buscar/', buscador_productos, name='buscar_productos'), #para llevarlo al html
]