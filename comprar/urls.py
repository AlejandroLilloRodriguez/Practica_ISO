from django.urls import path
from . import views

urlpatterns = [
    path('comprar/', views.comprar, name='comprar'), #para llevarlo al html
]