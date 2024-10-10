# carrito/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Producto, CarritoItem

def manejar_carrito(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)

        if action == 'agregar':
            # Lógica para agregar producto
            carrito_item, creado = CarritoItem.objects.get_or_create(producto=producto)
            if not creado:
                # Si el producto ya está en el carrito, incrementa la cantidad
                carrito_item.cantidad += 1
            carrito_item.save()

        elif action == 'eliminar':
            # Lógica para eliminar producto
            try:
                carrito_item = CarritoItem.objects.get(producto=producto)
                carrito_item.delete()
            except CarritoItem.DoesNotExist:
                pass  # El producto no estaba en el carrito

        elif action == 'modificar':
            # Lógica para modificar la cantidad de producto
            nueva_cantidad = int(request.POST.get('cantidad', 1))
            if nueva_cantidad > 0:
                carrito_item = CarritoItem.objects.get(producto=producto)
                carrito_item.cantidad = nueva_cantidad
                carrito_item.save()
            else:
                # Si la cantidad es 0, eliminar el producto del carrito
                carrito_item.delete()

    # Renderiza el carrito con los productos añadidos
    carrito_items = CarritoItem.objects.all()  # Obtiene todos los productos en el carrito
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})
