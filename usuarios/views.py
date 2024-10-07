# usuarios/views.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Definir el formulario de registro dentro de la vista
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Vista que maneja el inicio de sesión y registro
def mi_cuenta(request):
    if request.method == 'POST':
        # Si se envía el formulario de inicio de sesión
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
            else:
                messages.error(request, "Formulario de inicio de sesión inválido. Verifica los campos.")
        
        # Si se envía el formulario de registro
        elif 'register' in request.POST:
            registro_form = RegistroForm(request.POST)
            login_form = AuthenticationForm()  # Mantener el formulario de inicio de sesión vacío
            if registro_form.is_valid():
                user = registro_form.save()  # Crea el nuevo usuario
                login(request, user)  # Inicia la sesión automáticamente después del registro
                messages.success(request, "Registro exitoso")
                return redirect('inicio')  # Redirige a la página de inicio
            else:
                print(registro_form.errors)
                messages.error(request, "Error en el registro. Inténtalo de nuevo.")
    else:
        # Si la solicitud es GET
        login_form = AuthenticationForm()
        registro_form = RegistroForm()

    return render(request, 'Mi-cuenta.html', {
        'login_form': login_form,
        'registro_form': registro_form,
    })