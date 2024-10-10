from django import forms
from django.contrib.auth.models import User


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
    


class CambiarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']  # Solo permite cambiar el nombre de usuario

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username