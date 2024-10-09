from django.urls import path
from .views import mostrar_productos

urlpatterns = [
    path('productos/', mostrar_productos, name='productos'),
]