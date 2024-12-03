from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.db import connection
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@login_required
def comprar(request):
    # Verificar que el usuario está autenticado
    usuario_id = request.user.id
    usuario_email = request.user.email

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

    # Suponiendo que el pago es exitoso
    if request.method == 'POST':
        # Aquí podrías agregar la lógica del pago y verificar que sea exitoso

        # Renderizar la plantilla HTML para el correo
        asunto = "Confirmación de tu compra en el Comparador de Supermercados"
        mensaje_html = render_to_string('confirmacion_compra_email.html', {
            'username': request.user.username,
            'carrito_items': carrito_items.values(),
            'total_precio': total_precio,
        })

        # Crear el mensaje de correo
        try:
            email = EmailMultiAlternatives(
                asunto,
                '',  # Mensaje de texto plano, lo dejaremos vacío
                settings.DEFAULT_FROM_EMAIL,
                [usuario_email]
            )
            email.attach_alternative(mensaje_html, "text/html")
            email.send()

            # Mensaje de éxito en la interfaz
            return render(request, 'comprar.html', {'total_precio': total_precio, 'mensaje_exito': 'Compra realizada con éxito. Se ha enviado un correo con los detalles de tu compra.'})
        except Exception as e:
            # Mostrar mensaje de error en la interfaz si falla el envío del correo
            return render(request, 'comprar.html', {'total_precio': total_precio, 'mensaje_error': 'Hubo un error al enviar el correo de confirmación. Tu compra se realizó correctamente.'})

    return render(request, 'comprar.html', {'total_precio': total_precio})
