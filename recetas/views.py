from django.shortcuts import render


def recetas(request):
    return render(request, 'recetas.html')

# Create your views here.
