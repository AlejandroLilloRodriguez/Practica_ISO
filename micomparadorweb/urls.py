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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mi-cuenta/', usuario_views.mi_cuenta, name='mi_cuenta'),
    path('', principal_views.inicio, name='inicio'),
    path('supermercados/', supermercados_views.supermercado, name='supermercados'),
    path('productos/', productos_views.producto, name='productos'),
    path('reset-password/', usuario_views.reset_password, name='reset_password'),
]
