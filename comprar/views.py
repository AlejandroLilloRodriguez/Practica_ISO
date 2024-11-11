from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 

@login_required

def comprar(request):
    # Tu lógica para la vista de compra
    if not request.user.is_authenticated:
        return redirect('mi_compra')  # Redirigir al login si el usuario no está autenticado

    total = request.session.get('total_precio', 0)
    return render(request, 'comprar.html', {'total_precio': total})