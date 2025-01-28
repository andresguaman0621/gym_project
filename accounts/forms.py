from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida
from .models import ClientePerfil
import re

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Regex para validar el formato de correo electrónico
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format")

        # Verificar dominio
        dominios_populares = [
            "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
            "aol.com", "protonmail.com", "zoho.com", "mail.com", "yandex.com",
            "gmx.com", "msn.com", "live.com", "comcast.net", "me.com", "btinternet.com"
        ]
        dominio = email.split('@')[-1]
        if dominio not in dominios_populares:
            raise ValidationError(f"Email domain '{dominio}' is not allowed")

        # Verificar si ya existe el correo
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Validar longitud mínima
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        # Validar al menos una letra mayúscula
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        # Validar al menos una letra minúscula
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter")
        
        # Validar al menos un número
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit")
        
        # Validar al menos un carácter especial
        special_characters = "!@#$%^&*()-_+=<>?/|"
        if not any(char in special_characters for char in password):
            raise ValidationError(f"Password must contain at least one special character: {special_characters}")
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.date_joined = timezone.now()  
        if commit:
            user.save()
        return user

class SecretKeyForm(forms.Form):
    secret_key = forms.CharField(widget=forms.PasswordInput, label="Enter Secret Key")

    def clean_secret_key(self):
        secret_key = self.cleaned_data.get('secret_key')
        if secret_key != "MC60H-DWHD5-H80U9-6V85M-8280D":
            raise ValidationError("Invalid secret key.")
        return secret_key
      
class RutinaEntrenamientoForm(forms.ModelForm):
    class Meta:
        model = RutinaEntrenamiento
        fields = ['cliente', 'fecha_inicio', 'fecha_fin']

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'series', 'repeticiones', 'peso_recomendado']


class PlanAlimentacionForm(forms.ModelForm):
    class Meta:
        model = PlanAlimentacion
        fields = ['cliente', 'fecha_inicio', 'fecha_fin']

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Comida
        fields = ['tipo', 'hora', 'nombre', 'cantidad', 'unidad']
        
class FormularioFactory:
    """
    Factory Method para crear formularios de modelos.
    """

    @staticmethod
    def crear_formulario(tipo):
        if tipo == "rutina":
            return RutinaEntrenamientoForm
        elif tipo == "ejercicio":
            return EjercicioForm
        elif tipo == "plan_alimentacion":
            return PlanAlimentacionForm
        elif tipo == "comida":
            return ComidaForm
        else:
            raise ValueError(f"Tipo de formulario '{tipo}' no es válido")


# class ClientePerfilForm(forms.ModelForm):
#     class Meta:
#         model = ClientePerfil
#         fields = ['peso', 'altura', 'objetivo']

class ClientePerfilForm(forms.ModelForm):
    class Meta:
        model = ClientePerfil
        fields = ['peso', 'altura', 'objetivo', 'genero']

