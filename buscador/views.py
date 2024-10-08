from django.shortcuts import render
from .models import ProductoTablaAlcampo, ProductoTablaCarrefour, ProductoTablaEroski
# Create your views here.
def buscador_productos(request):
    print("La vista buscar_productos se ha llamado")
    query= request.GET.get('s', '').strip()
    print(f"Consulta de búsqueda: {query}")
    resultados = []

    if query:
        resultados += list(ProductoTablaAlcampo.objects.filter(nombre__icontains = query))
        resultados +=list(ProductoTablaCarrefour.objects.filter(nombre__icontains = query))
        resultados +=list(ProductoTablaEroski.objects.filter(nombre__icontains = query))
    print(f"Resultados encontrados: {resultados}") 
    
    return render(request, 'resultados_busqueda.html', {'resultados': resultados, 'query': query})