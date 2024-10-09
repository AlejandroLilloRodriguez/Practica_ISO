from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.annadir_a_carrito, name='annadir_a_carrito'),
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('remove/<int:cart_item_id>/', views.borrar_de_carrito, name='borrar_de_carrito'),
    path('update/<int:cart_item_id>/<int:quantity>/', views.actualizar_carrito, name='actualizar_carrito'),
]
