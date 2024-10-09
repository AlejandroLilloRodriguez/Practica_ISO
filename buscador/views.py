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
        palabras_buscadas = query.split()

        # Crear una consulta con Q objects para que cada palabra se busque en el nombre
        consulta = Q()
        for palabra in palabras_buscadas:
            consulta &= (
                Q(nombre__icontains=palabra)
            )

    if query:
        resultados += list(ProductoTablaAlcampo.objects.filter(consulta))
        resultados +=list(ProductoTablaCarrefour.objects.filter(consulta))
        resultados +=list(ProductoTablaEroski.objects.filter(consulta))
    print(f"Resultados encontrados: {resultados}") 
    
    if ordenar_por == 'precio':
        if direccion == 'asc':
            resultados.sort(key=lambda producto: producto.precio)
        else:
            resultados.sort(key=lambda producto: producto.precio, reverse=True)
    elif ordenar_por == 'precio_por_kg':
        if direccion == 'asc':
            resultados.sort(key=lambda producto: producto.precio_por_kg)
        else:
            resultados.sort(key=lambda producto: producto.precio_por_kg, reverse=True)
    return render(request, 'resultados_busqueda.html', {'resultados': resultados, 'query': query})