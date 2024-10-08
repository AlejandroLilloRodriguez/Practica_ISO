from django import forms
from django.contrib.auth.models import User

class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Nueva contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar nueva contraseña")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data