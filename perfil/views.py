from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Definir el formulario para cambiar el usuario y el email
class CambiarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email ya está en uso.")
        return email

@login_required
def perfil(request):
    user = request.user

    if request.method == 'POST':
        form = CambiarPerfilForm(request.POST, instance=user)
        if form.is_valid():
            # Guardar los cambios del perfil
            user = form.save(commit=False)  # No guardar inmediatamente
            user.email = form.cleaned_data['email']  # Asegurarse de que el correo sea el correcto
            user.username = form.cleaned_data['username']
            user.save()  # Guardar el usuario actualizado en la base de datos
            
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil')  # Redirige a la misma página del perfil
        else:
            # Mostrar mensaje de error en caso de no validarse el formulario
            messages.error(request, 'Introduzca otros datos.')
    else:
        form = CambiarPerfilForm(instance=user)

    return render(request, 'perfil.html', {
        'form': form,
        'usuario': user  # Asegúrate de pasar el usuario al template
    })

# Formulario para restablecer contraseña
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Nueva contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar nueva contraseña")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)  # Establece la nueva contraseña
            user.save()

            # Vuelve a autenticar al usuario
            authenticated_user = authenticate(username=user.username, password=new_password)
            if authenticated_user is not None:
                login(request, authenticated_user)  # Vuelve a iniciar sesión
                messages.success(request, 'Contraseña restablecida con éxito.')
                return redirect('perfil')  # Redirige al perfil
            else:
                messages.error(request, 'Error al volver a autenticar. Por favor, inicia sesión nuevamente.')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})
