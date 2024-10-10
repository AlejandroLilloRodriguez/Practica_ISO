from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

# Si deseas permitir que el usuario edite su perfil, puedes crear un formulario personalizado
class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Vista para ver o editar el perfil
@login_required  # Asegura que solo los usuarios autenticados puedan acceder
def perfil(request):
    user = request.user

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Guarda los cambios del perfil
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil')  # Redirige a la misma página del perfil
    else:
        form = PerfilForm(instance=user)

    return render(request, 'perfil.html', {'form': form})