from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.core.mail import send_mail



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

    # Cálculo de la fecha de entrega (sumando 4 o 5 días a la fecha actual)
    fecha_compra = datetime.now()
    fecha_entrega = fecha_compra + timedelta(days=5)  # Sumar 5 días a la fecha actual

    if request.method == 'POST':
        # Aquí podrías agregar la lógica del pago y verificar que sea exitoso

        # Renderizar la plantilla HTML para el correo
        asunto = "Confirmación de tu compra en el Comparador de Supermercados"
        mensaje_html = render_to_string('confirmacion_compra_email.html', {
            'username': request.user.username,
            'carrito_items': carrito_items.values(),
            'total_precio': total_precio,
            'fecha_entrega': fecha_entrega.strftime('%d/%m/%Y'),  # Pasar la fecha de entrega como string
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

            # Limpiar el carrito después de una compra exitosa (si el pago es exitoso)
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", [usuario_id])

            # Redirigir a la página de compra exitosa
            return redirect('compra_exitosa')

        except Exception as e:
            # Mostrar mensaje de error en la interfaz si falla el envío del correo
            return render(request, 'comprar.html', {'total_precio': total_precio, 'mensaje_error': 'Hubo un error al enviar el correo de confirmación. Tu compra se realizó correctamente.'})

    return render(request, 'comprar.html', {'total_precio': total_precio})



def compra_exitosa(request):
    # Renderizar la página de compra exitosa
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
        # Aquí puedes agregar la lógica para procesar el pago

        # Enviar correo al usuario indicando que la compra fue exitosa
        try:
            subject = 'Compra Exitosa'
            message = 'Gracias por tu compra. Tu pedido ha sido procesado correctamente.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]  # Correo del usuario

            send_mail(subject, message, from_email, recipient_list)

            # Redirigir al usuario a la página de inicio o a donde desees
            return redirect('inicio')

        except Exception as e:
            return HttpResponse(f'Error al enviar el correo: {str(e)}')

    return render(request, 'comprar.html')
