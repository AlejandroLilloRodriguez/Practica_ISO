from django.urls import path
from . import views

urlpatterns = [
    path('comprar/', views.comprar, name='comprar'), #para llevarlo al html
    path('direccion/', views.direccion_envio, name='direccion_envio'),
    path('pago/', views.datos_pago, name='datos_pago'),
    path('direccion/', views.direccion_envio, name='direccion_envio'),
    path('datos-pago/', views.datos_pago, name='datos_pago'),
    path('', views.comprar, name='comprar'),
    path('compra-exitosa/', views.compra_exitosa, name='compra_exitosa'),
    
]