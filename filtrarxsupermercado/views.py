from django.shortcuts import render
from buscador.models import ProductoTablaEroski, ProductoTablaCarrefour, ProductoTablaAlcampo
# Create your views here.
def productos_por_supermercado(request, supermercado):
    # Filtrar productos según el supermercado
    if supermercado.lower() == 'eroski':
        productos = ProductoTablaEroski.objects.all()
    elif supermercado.lower() == 'carrefour':
        productos = ProductoTablaCarrefour.objects.all()
    elif supermercado.lower() == 'alcampo':
        productos = ProductoTablaAlcampo.objects.all()
    else:
        productos = []  # Si no coincide con ninguno, devolvemos una lista vacía.

    return render(request, 'resultados_busqueda.html', {
        'productos': productos,
        'supermercado': supermercado
    })