
# views.py

from django.shortcuts import render, get_object_or_404
from .models import Receta

def ingredientes(request, receta_id):
    # Obtener la receta por su id
    receta = get_object_or_404(Receta, pk=receta_id)
    
    # Obtener los ingredientes relacionados con la receta
    ingredientes = receta.ingredientes.all()

    return render(request, 'ingredientes.html', {'receta': receta, 'ingredientes': ingredientes})

# Create your views here.
# urls.py

