from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta



@login_required
def comprar(request):
    usuario_id = request.user.id

    # Obtener los items del carrito
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT producto_id, nombre, precio, precio_por_kg, supermercado, imagen, cantidad
            FROM carrito WHERE usuario_id = %s
        """, [usuario_id])
        columns = [col[0] for col in cursor.description]
        carrito_items = [dict(zip(columns, row)) for row in cursor.fetchall()]
        carrito_items = {item['producto_id']: item for item in carrito_items}

    # Calcular el total_precio
    total_precio = sum(item['precio'] * item['cantidad'] for item in carrito_items.values())

    if request.method == 'POST':
        # Recuperar la dirección de envío desde la sesión
        direccion_envio = request.session.get('direccion')
        ciudad_envio = request.session.get('ciudad')

        # Calcular fechas
        fecha_compra = datetime.now().strftime('%d/%m/%Y')
        fecha_entrega = (datetime.now() + timedelta(days=5)).strftime('%d/%m/%Y')

        # Limpiar el carrito después de una compra exitosa
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", [usuario_id])

        # Redirigir a una página de confirmación
        return redirect('compra_exitosa')

    return render(request, 'comprar.html', {'total_precio': total_precio})

def compra_exitosa(request):
    return render(request, 'compra_exitosa.html')



def direccion_envio(request):
    if request.method == 'POST':
        # Guardar la dirección de envío en la sesión
        request.session['direccion'] = request.POST.get('address')
        request.session['ciudad'] = request.POST.get('city')
        return redirect('datos_pago')
    return render(request, 'envio.html')

def datos_pago(request):
    if request.method == 'POST':
        # Procesar los datos de pago aquí
        return redirect('inicio')  # Por ejemplo, redirigir al inicio si el pago es exitoso
    return render(request, 'comprar.html')
