from django.shortcuts import render
from .models import ProductoTablaAlcampo, ProductoTablaCarrefour, ProductoTablaEroski
# Create your views here.
def buscador_productos(request):
    query= request.GET.get('search')
    print(f"Consulta de búsqueda: {query}")
    resultados = []

    if query:
        resultados +=ProductoTablaAlcampo.filter(nombre__icontains = query)
        resultados +=ProductoTablaCarrefour.filter(nombre__icontains = query)
        resultados +=ProductoTablaEroski.filter(nombre__icontains = query)
    print(f"Resultados encontrados: {resultados}") 
    
    return render(request, 'resultados_busqueda.html', {'resultados': resultados, 'query': query})