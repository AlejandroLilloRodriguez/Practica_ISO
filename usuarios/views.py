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

# Formulario para cambiar usuario y email
class CambiarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Campos a actualizar

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

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

                # Verificar si el usuario se autentica correctamente
                if user is not None:
                    login(request, user)
                    messages.success(request, "Inicio de sesión realizado exitosamente.")
                    return redirect('perfil')  # Redirige a la página de perfil
                else:
                    messages.error(request, "Usuario o contraseña incorrectos")  # Solo se muestra si no se autentica
            else:
                messages.error(request, "Formulario de inicio de sesión inválido. Verifica los campos.")  # Mensaje de error si el formulario no es válido

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
        usuario = request.user
        form = CambiarUsuarioForm(request.POST, instance=usuario)  # Usar el nuevo formulario

        if form.is_valid():
            form.save()  # Guarda el nuevo nombre de usuario y email
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect('perfil')  # Redirigir a la página del perfil
    else:
        form = CambiarUsuarioForm(instance=request.user)  # Cargar el formulario con el usuario actual

    return render(request, 'perfil.html', {
        'form': form,
        'usuario': request.user  # Pasamos el usuario autenticado al template
    })
