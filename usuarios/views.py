from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .forms import ResetPasswordForm


# Definir el formulario de registro dentro de la vista
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Solo puede haber un usuario por correo
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email


# Vista que maneja el inicio de sesión y registro
def mi_cuenta(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        # Manejo del formulario de inicio de sesión
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            registro_form = RegistroForm()  # Mantener el formulario de registro vacío
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Bienvenido, {username}")
                    return redirect('inicio')  # Redirige a la página de inicio
                else:
                    messages.error(request, "Usuario o contraseña incorrectos")
        
        # Manejo del formulario de registro
        elif 'register' in request.POST:
            registro_form = RegistroForm(request.POST)
            login_form = AuthenticationForm()  # Mantener el formulario de inicio de sesión vacío
            if registro_form.is_valid():
                user = registro_form.save()  # Crea el nuevo usuario
                login(request, user)  # Inicia la sesión automáticamente después del registro
                messages.success(request, "Registro exitoso")
                return redirect('inicio')  # Redirige a la página de inicio
            else:
                messages.error(request, "Error en el registro. Inténtalo de nuevo.")
    else:
        login_form = AuthenticationForm()
        registro_form = RegistroForm()

    return render(request, 'Mi-cuenta.html', {
        'login_form': login_form,
        'registro_form': registro_form,
    })


# Vista para restablecer contraseña
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_password = form.cleaned_data.get('new_password')

            try:
                user = User.objects.get(username=username)
                user.password = make_password(new_password)  # Encriptar la nueva contraseña
                user.save()
                messages.success(request, f'La contraseña ha sido restablecida para el usuario {username}.')
                return redirect('inicio')  # Redirigir a la página de inicio u otra página
            except User.DoesNotExist:
                messages.error(request, 'El nombre de usuario no existe.')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})


# Vista para editar perfil (accesible solo si está autenticado)
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Obtener el usuario actual
        usuario = request.user

        # Obtener los nuevos datos enviados por el formulario
        nuevo_username = request.POST.get('username')
        nueva_password = request.POST.get('password')
        nueva_password_confirm = request.POST.get('password_confirm')

        # Verificar si el nombre de usuario cambió
        if nuevo_username and nuevo_username != usuario.username:
            # Actualizar el nombre de usuario
            if User.objects.filter(username=nuevo_username).exists():
                messages.error(request, "El nombre de usuario ya está en uso.")
            else:
                usuario.username = nuevo_username
                messages.success(request, "Nombre de usuario actualizado.")

        # Verificar si la contraseña cambió y es válida
        if nueva_password and nueva_password == nueva_password_confirm:
            usuario.password = make_password(nueva_password)
            messages.success(request, "Contraseña actualizada con éxito.")
        elif nueva_password and nueva_password != nueva_password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")

        # Guardar los cambios en el usuario
        usuario.save()

        return redirect('perfil')

    return render(request, 'perfil.html', {
        'usuario': request.user  # Pasamos el usuario autenticado al template
    })