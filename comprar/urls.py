from django.urls import path
from . import views

urlpatterns = [
    path('comprar/', views.comprar, name='comprar'), #para llevarlo al html
    path('direccion/', views.direccion_envio, name='direccion_envio'),
    path('pago/', views.datos_pago, name='datos_pago'),
]