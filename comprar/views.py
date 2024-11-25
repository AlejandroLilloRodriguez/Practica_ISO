from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.db import connection

@login_required
def comprar(request):
    # Verificar que el usuario está autenticado
    usuario_id = request.user.id

    # Obtener los items del carrito
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT producto_id, nombre, precio, precio_por_kg, supermercado, imagen, cantidad
            FROM carrito WHERE usuario_id = %s
        """, [usuario_id])
        columns = [col[0] for col in cursor.description]
        carrito_items = [
            dict(zip(columns, row)) for row in cursor.fetchall()
        ]
        carrito_items = {item['producto_id']: item for item in carrito_items}

    # Calcular el total_precio
    total_precio = sum(item['precio'] * item['cantidad'] for item in carrito_items.values())

    return render(request, 'comprar.html', {'total_precio': total_precio})
