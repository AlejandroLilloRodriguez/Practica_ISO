from django.shortcuts import render
from buscador.models import ProductoTablaAlcampo, ProductoTablaCarrefour, ProductoTablaEroski
# Create your views here.

def mostrar_productos(request):
    # Obtener todos los productos de las diferentes tablas
    productos_alcampo = ProductoTablaAlcampo.objects.all()
    productos_carrefour = ProductoTablaCarrefour.objects.all()
    productos_eroski = ProductoTablaEroski.objects.all()
    
    # Combinar todos los productos en una sola lista
    todos_productos = list(productos_alcampo) + list(productos_carrefour) + list(productos_eroski)

    # Renderizar la plantilla con la lista de productos
    return render(request, 'productos.html', {'productos': todos_productos})