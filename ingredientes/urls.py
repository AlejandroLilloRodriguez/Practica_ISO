from django.urls import path
from . import views

urlpatterns = [
    path('ingredientes/<int:receta_id>/', views.ingredientes, name='ingredientes'),
]
