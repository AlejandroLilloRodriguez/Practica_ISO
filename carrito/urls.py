# carrito/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.vista_carrito, name='vista_carrito'),
]
