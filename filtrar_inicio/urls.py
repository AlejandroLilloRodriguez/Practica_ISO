from django.urls import path
from . import views

urlpatterns = [
    path('productos/<str:categoria>/', views.filtrar_productos, name='filtrar_productos'),
]
