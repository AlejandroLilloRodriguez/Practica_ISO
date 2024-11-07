from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 

@login_required

def comprar(request):
    # Tu lógica para la vista de compra
    if not request.user.is_authenticated:
        return redirect('mi_compra')  # Redirigir al login si el usuario no está autenticado

    # Lógica para el proceso de compra
    # ...

    return render(request, 'comprar.html')
