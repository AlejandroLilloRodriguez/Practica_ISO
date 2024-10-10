# carrito/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.manejar_carrito, name='carrito'),
  #  path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
#  path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
  #  path('modificar/<int:producto_id>/', views.modificar_producto, name='modificar_producto'),
]
