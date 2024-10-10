from django.urls import path
from .views import views

urlpatterns = [
    path('perfil/', views.perfil , name='perfil'),
]