from django.shortcuts import render

# Create your views here.

def producto(request):
    return render(request, 'PRODUCTOS.html')