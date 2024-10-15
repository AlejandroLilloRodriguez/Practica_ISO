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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_bytes
from .forms import ResetPasswordForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import update_session_auth_hash  # Para mantener la sesión activa




email_template_name = "password_reset_email.html"




# Definir el formulario de registro dentro de la vista
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

# Formulario para cambiar usuario y email
class CambiarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

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
            registro_form = RegistroForm()
            
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, "Inicio de sesión realizado exitosamente.")
                    return redirect('inicio')
                else:
                    messages.error(request, "Usuario o contraseña incorrectos.")
            else:
                messages.error(request, "Formulario de inicio de sesión inválido.")

        # Manejo del formulario de registro
        elif 'register' in request.POST:
            registro_form = RegistroForm(request.POST)
            login_form = AuthenticationForm()
            if registro_form.is_valid():
                user = registro_form.save()
                login(request, user)
                messages.success(request, "Registro exitoso")
                return redirect('inicio')
            else:
                messages.error(request, "Error en el registro. Inténtalo de nuevo.")
    else:
        login_form = AuthenticationForm()
        registro_form = RegistroForm()

    return render(request, 'Mi-cuenta.html', {
        'login_form': login_form,
        'registro_form': registro_form,
    })

# Vista para solicitar el restablecimiento de la contraseña
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            subject = "Restablecimiento de Contraseña"
            email_template_name = "password_reset_email.html"
            context = {
                "email": user.email,
                "domain": request.get_host(),
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            email_content = render_to_string(email_template_name, context)
            send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            messages.success(request, "Se ha enviado un enlace para restablecer la contraseña a tu correo electrónico.")
        except User.DoesNotExist:
            messages.error(request, "No existe un usuario con ese correo electrónico.")
    return render(request, "password_reset_form.html")


# Vista para confirmar el restablecimiento de la contraseña
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Tu contraseña ha sido restablecida exitosamente.')
            return redirect('mi_cuenta')
        return render(request, 'password_reset_confirm.html')
    else:
        messages.error(request, 'El enlace para restablecer la contraseña es inválido.')
        return redirect('mi_cuenta')

# Vista para restablecer contraseña (opcional, si deseas incluir esta vista)
@login_required
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Contraseña actualizada con éxito.')
            return redirect('perfil')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})

# Vista para editar perfil
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        usuario = request.user
        form = CambiarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect('perfil')
    else:
        form = CambiarUsuarioForm(instance=request.user)

    return render(request, 'perfil.html', {
        'form': form,
        'usuario': request.user
    })

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()

                # Cerrar todas las sesiones del usuario
                all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if str(user.pk) == str(session_data.get('_auth_user_id')):
                        session.delete()

                # Enviar mensaje de éxito
                messages.success(request, "Tu contraseña ha sido restablecida exitosamente y se ha cerrado la sesión en todos los dispositivos.")
                return redirect("mi_cuenta")
            else:
                messages.error(request, "Las contraseñas no coinciden. Intenta de nuevo.")
    else:
        messages.error(request, "El enlace para restablecer la contraseña no es válido o ha expirado.")
    
    return render(request, "password_reset_confirm.html")
