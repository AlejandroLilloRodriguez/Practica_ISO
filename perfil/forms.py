from django import forms
from django.contrib.auth.models import User

class CambiarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Incluye los campos que quieres cambiar
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nuevo nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Nuevo correo electrónico'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar los errores de validación predeterminados
        for field in self.fields.values():
            field.error_messages = {'required': 'Este campo es obligatorio.'}  # Mensaje de error personalizado
