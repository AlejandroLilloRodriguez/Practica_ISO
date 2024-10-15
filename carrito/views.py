# carrito/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Producto
from django.contrib.auth.decorators import login_required
import hashlib

def generar_id_producto(producto):
    # Usa el nombre y precio para generar un hash único para cada producto
    data = f"{producto['nombre']}{producto['precio']}"
    return hashlib.md5(data.encode()).hexdigest()

def limpiar_precio(precio_str):
    # Eliminar símbolos de moneda y caracteres no deseados
    precio_limpio = precio_str.replace('€', '').replace(',', '.').replace('\xa0', '').replace(' ', '').strip()
    try:
        # Convertir a float
        return float(precio_limpio)
    except ValueError:
        # Manejo de errores si el precio no se puede convertir
        print(f"Error convirtiendo precio: {precio_str}")  # Para depuración
        return 0.0
    
@login_required
def manejar_carrito(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        producto_nombre = request.POST.get('producto_nombre')
        producto_precio = request.POST.get('producto_precio')
        producto_precio_por_kg = request.POST.get('producto_precio_por_kg')  # Añadido
        producto_imagen = request.POST.get('producto_imagen')  # Añadido
        producto_supermercado = request.POST.get('producto_supermercado')  # Añadido

        # Limpiar el precio y convertirlo en float
        producto_precio_float = limpiar_precio(producto_precio)

        # Generar un ID único para el producto
        producto_id = generar_id_producto({'nombre': producto_nombre, 'precio': producto_precio_float})

        # Inicializar carrito en la sesión si no existe
        if 'carrito' not in request.session:
            request.session['carrito'] = {}
        
        carrito = request.session['carrito']

        if action == 'agregar':
            if producto_id in carrito:
                carrito[producto_id]['cantidad'] += 1
            else:
                # Añadir producto con cantidad 1
                carrito[producto_id] = {
                    'supermercado': producto_supermercado,
                    'nombre': producto_nombre,
                    'precio': producto_precio_float,  # Ya está limpio
                    'cantidad': 1,
                    'imagen': producto_imagen,
                    'precio_por_kg': producto_precio_por_kg
                }

            print(f"Carrito actualizado: {carrito}")

        elif action == 'eliminar':
            if producto_id in carrito:
                del carrito[producto_id]

        elif action == 'modificar':
            nueva_cantidad = int(request.POST.get('cantidad', 1))
            if nueva_cantidad > 0:
                carrito[producto_id]['cantidad'] = nueva_cantidad
            else:
                del carrito[producto_id]

        # Guardar los cambios en la sesión
        request.session['carrito'] = carrito

    # Renderizar el carrito con los productos añadidos
    carrito_items = request.session.get('carrito', {})

    # Calcular el total
    total = 0
    for item in carrito_items.values():
        # Asegúrate de que 'precio' y 'cantidad' están en el item
        if 'precio' in item and 'cantidad' in item:
            # El precio ya está limpio, no es necesario limpiarlo de nuevo
            item_precio = item['precio']  # Ya debería ser float
            item_cantidad = int(item['cantidad'])  # Asegúrate de que sea un entero
            item_total = item_precio * item_cantidad  # Calcular el total por item
            total += item_total  # Acumular el total

            # Imprimir dentro del bucle para evitar errores
            print(f"Precio: {item['precio']}, Tipo: {type(item['precio'])}")
            print(f"Cantidad: {item['cantidad']}, Tipo: {type(item['cantidad'])}")
        else:
            print(f"Item no válido: {item}")

    # Redirige a la página donde se muestra el carrito con los productos añadidos
    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})
