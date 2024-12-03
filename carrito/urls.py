# carrito/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.manejar_carrito, name='carrito'),
    
]
