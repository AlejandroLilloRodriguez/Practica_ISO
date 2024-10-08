from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscador_productos, name='buscar_productos'), #para llevarlo al html
]