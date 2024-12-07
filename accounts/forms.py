from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida, Alimento
from .models import ClientePerfil

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.date_joined = timezone.now()  # Sets the current date and time
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
        fields = ['rutina', 'nombre', 'series', 'repeticiones', 'peso_recomendado']

class PlanAlimentacionForm(forms.ModelForm):
    class Meta:
        model = PlanAlimentacion
        fields = ['cliente', 'fecha_inicio', 'fecha_fin']

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Comida
        fields = ['plan', 'tipo', 'hora']

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['comida', 'nombre', 'cantidad', 'unidad']


class ClientePerfilForm(forms.ModelForm):
    class Meta:
        model = ClientePerfil
        fields = ['peso', 'altura', 'objetivo']
