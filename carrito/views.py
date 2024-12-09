import uuid
from django.db import connection
from django.utils.timezone import now, timedelta
from django.shortcuts import render, redirect
import hashlib
from django.middleware.csrf import get_token


def limpiar_carritos_caducados():
    """
    Elimina los productos del carrito que tengan más de 1 hora de antigüedad.
    """
    limite_tiempo = now() - timedelta(hours=1)
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM carrito
            WHERE fecha_creacion < %s
        """, [limite_tiempo])

def generar_id_producto(producto):
    """
    Genera un hash único para identificar cada producto.
    """
    data = f"{producto['nombre']}{producto['precio']}"
    return hashlib.md5(data.encode()).hexdigest()

def limpiar_precio(precio_str):
    """
    Limpia y convierte un precio a formato float.
    """
    try:
        if isinstance(precio_str, (float, int)):
            return float(precio_str)
        return float(str(precio_str).replace('€', '').replace(',', '.').replace('\xa0', '').replace(' ', '').strip())
    except ValueError:
        return 0.0

def manejar_carrito(request):
    # Verificar si la sesión está activa
    if not request.session.session_key:
        # Si la sesión está caducada, crear una nueva sesión
        request.session.create()

    # Asegurarse de que el token CSRF es válido
    csrf_token = get_token(request)

    # Identificar el carrito por cookie_id o usuario_id
    cookie_id = request.COOKIES.get('carrito_id', str(uuid.uuid4()))
    usuario_id = request.user.id if request.user.is_authenticated else None

    if request.method == 'POST':
        action = request.POST.get('action')
        producto_nombre = request.POST.get('producto_nombre')
        producto_precio = limpiar_precio(request.POST.get('producto_precio'))
        producto_precio_por_kg = limpiar_precio(request.POST.get('producto_precio_por_kg'))
        producto_imagen = request.POST.get('producto_imagen')
        producto_supermercado = request.POST.get('producto_supermercado')
        producto_id = generar_id_producto({'nombre': producto_nombre, 'precio': producto_precio})

        if action == 'agregar':
            if request.user.is_authenticated:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO carrito (cookie_id, usuario_id, producto_id, nombre, precio, precio_por_kg,
                                             supermercado, imagen, cantidad, fecha_creacion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE cantidad = cantidad + 1
                    """, [cookie_id, usuario_id, producto_id, producto_nombre, producto_precio, producto_precio_por_kg,
                          producto_supermercado, producto_imagen, 1, now()])
            else:
                carrito = request.session.get('carrito', {})
                if producto_id in carrito:
                    carrito[producto_id]['cantidad'] += 1
                else:
                    carrito[producto_id] = {
                        'nombre': producto_nombre,
                        'precio': producto_precio,
                        'precio_por_kg': producto_precio_por_kg,
                        'supermercado': producto_supermercado,
                        'imagen': producto_imagen,
                        'cantidad': 1,
                    }
                request.session['carrito'] = carrito

        elif action == 'eliminar':
            if request.user.is_authenticated:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM carrito WHERE usuario_id = %s AND producto_id = %s
                    """, [usuario_id, producto_id])
            else:
                carrito = request.session.get('carrito', {})
                if producto_id in carrito:
                    del carrito[producto_id]
                request.session['carrito'] = carrito

    # Sincronizar carrito en la sesión con el carrito del usuario autenticado
    if request.user.is_authenticated and 'carrito' in request.session:
        for producto_id, item in request.session['carrito'].items():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO carrito (cookie_id, usuario_id, producto_id, nombre, precio, precio_por_kg,
                                         supermercado, imagen, cantidad, fecha_creacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)
                """, [cookie_id, usuario_id, producto_id, item['nombre'], item['precio'], item['precio_por_kg'],
                      item['supermercado'], item['imagen'], item['cantidad'], now()])
        del request.session['carrito']

    # Obtener carrito para renderizar
    if request.user.is_authenticated:
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
    else:
        carrito_items = request.session.get('carrito', {})

    # Calcular total
    total_precio = sum(item['precio'] * item['cantidad'] for item in carrito_items.values())

    # Configurar respuesta
    response = render(request, 'carrito.html', {'carrito_items': carrito_items, 'total_precio': total_precio})
    response.set_cookie('carrito_id', cookie_id, max_age=3600, httponly=True, samesite='Lax')
    return response

