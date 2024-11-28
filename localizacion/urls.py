from django.urls import path
from . import views

urlpatterns = [
    path('supermercados-cercanos/', views.supermercados_cercanos, name='supermercados_cercanos'),
]