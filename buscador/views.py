from django.shortcuts import render
from .models import ProductoTablaAlcampo, ProductoTablaCarrefour, ProductoTablaEroski
from django.db.models import Q
# Create your views here.
def buscador_productos(request):
    print("La vista buscar_productos se ha llamado")
    query= request.GET.get('s', '').strip()
    ordenar_por = request.GET.get('ordenar_por', 'precio')
    direccion = request.GET.get('direccion', 'asc')
    print(f"Consulta de búsqueda: {query}")
    resultados = []

    if query:
        # Dividir la búsqueda en palabras para buscar cada una por separado
        palabras = query.split()

        productos_encontrados = set()

        # Función para filtrar productos
        def filtrar_productos(productos):
            for producto in productos:
                # Obtener el nombre del producto en minúsculas
                nombre_producto = producto.nombre.lower()
                # Verificar si todas las palabras están en el nombre del producto
                if all(palabra in nombre_producto.split() for palabra in palabras):
                    productos_encontrados.add(producto)

        # Filtrar productos de cada tabla
        filtrar_productos(ProductoTablaAlcampo.objects.all())
        filtrar_productos(ProductoTablaCarrefour.objects.all())
        filtrar_productos(ProductoTablaEroski.objects.all())

        productos = list(productos_encontrados)

    print(f"Resultados encontrados: {productos}") 
    
    if ordenar_por == 'precio':
        if direccion == 'asc':
            productos.sort(key=lambda producto: producto.precio)
        else:
            productos.sort(key=lambda producto: producto.precio, reverse=True)
    elif ordenar_por == 'precio_por_kg':
        if direccion == 'asc':
            productos.sort(key=lambda producto: producto.precio_por_kg)
        else:
            productos.sort(key=lambda producto: producto.precio_por_kg, reverse=True)
    return render(request, 'resultados_busqueda.html', {'productos': productos, 'query': query})