# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import ClientePerfil

class SuperAdministrador(User):
    def save(self, *args, **kwargs):
        if SuperAdministrador.objects.exists() and not self.pk:
            raise ValidationError("Solo puede existir un superadministrador.")
        super().save(*args, **kwargs)

class Ejercicio(models.Model):

    administrador = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='ejercicios_creados'
    )
    nombre = models.CharField(max_length=100)
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    peso_recomendado = models.FloatField()

    def __str__(self):
        return str(self.nombre)

class RutinaEntrenamiento(models.Model):
    cliente = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Relación con el usuario
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ejercicios = models.ManyToManyField(Ejercicio, related_name='rutinas', blank=True)  # Relación con ejercicios

    def __str__(self):
        return f'Rutina for {self.cliente.username} from {self.fecha_inicio} to {self.fecha_fin}'

class PlanAlimentacion(models.Model):
    cliente = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comidas = models.ManyToManyField('Comida', related_name='planes', blank=True)  # Relación con Comida

    def __str__(self):
        return f'Plan Alimentacion for {self.cliente.username} from {self.fecha_inicio} to {self.fecha_fin}'


class Comida(models.Model):
    # plan = models.ForeignKey(PlanAlimentacion, on_delete=models.CASCADE, related_name='comidas')
    tipo = models.CharField(max_length=50)
    hora = models.TimeField()
    nombre = models.CharField(max_length=100)  # Detalle del alimento
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre} ({self.cantidad} {self.unidad})'


# MODELO CLIENTE

class ClientePerfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    objetivo = models.CharField(
        max_length=50,
        choices=[('fuerza', 'Fuerza'), ('resistencia', 'Resistencia'), ('pérdida de peso', 'Pérdida de peso')],
        null=True,
        blank=True
    )
    genero = models.CharField(
        max_length=10,
        choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')],
        null=True,
        blank=True
    )
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


    
# REGISTRO CLIENTE
@receiver(post_save, sender=User)
def crear_perfil_cliente(sender, instance, created, **kwargs):
    if created:  # Solo se ejecuta al crear un usuario por primera vez
        ClientePerfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_cliente(sender, instance, **kwargs):
    instance.perfil.save()  # Asegura que el perfil se guarde al guardar el usuario
    
# NUEVO MODELO MENSAJES
class Mensaje(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mensaje de {self.cliente.username} en {self.fecha_envio}"
