"""
URL configuration for micomparadorweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuarios import views as usuario_views
from principal import views as principal_views
from supermercados import views as supermercados_views
from productos import views as productos_views
from buscador import views as buscar_views
from carrito import views as carrito_views
from filtrar_inicio import views as filtrar_inicio_views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios import views
from perfil import views as perfil_views
from comprar import views as comprar_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mi-cuenta/', usuario_views.mi_cuenta, name='mi_cuenta'),
    path('', principal_views.inicio, name='inicio'),
    path('supermercados/', supermercados_views.supermercado, name='supermercados'),
    path('productos/', productos_views.mostrar_productos, name='productos'),
    path('reset-password/', usuario_views.password_reset_request, name='reset_password'),
    path('buscador/',buscar_views.buscador_productos, name='buscar_productos'),
    path('carrito/', carrito_views.manejar_carrito, name='carrito'),
    path('perfil/', include('perfil.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('reset-password/', views.password_reset_request, name='usuarios_reset_password'),  # Cambia el nombre aquí
    path('reset-password-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),  # Agrega esta línea
    path('filtrarxsupermercado/', include('filtrarxsupermercado.urls')),
    path('filtrar_inicio/', include('filtrar_inicio.urls')),
    path('comprar/', include('comprar.urls')),



    
]
