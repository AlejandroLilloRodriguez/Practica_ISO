# filtrarxsupermercado/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/<str:supermercado>/', views.productos_por_supermercado, name='productos_supermercado'),
]