from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Definir el formulario para cambiar el usuario y el email
class CambiarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Añadimos el campo email también

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

@login_required
def perfil(request):
    user = request.user

    if request.method == 'POST':
        form = CambiarPerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Guarda los cambios del perfil
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil')  # Redirige a la misma página del perfil
    else:
        form = CambiarPerfilForm(instance=user)

    return render(request, 'perfil.html', {
        'form': form,
        'usuario': user  # Asegúrate de pasar el usuario al template
    })
