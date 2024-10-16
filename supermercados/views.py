from django.shortcuts import render


# Create your views here.

def supermercado(request):
    return render(request, 'SUPERMERCADOS.html')