# accounts/models.py

from django.db import models
from django.contrib.auth.models import User


class RutinaEntrenamiento(models.Model):
    cliente = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming cliente is a user
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __str__(self):
        return f'Rutina for {self.cliente} from {self.fecha_inicio} to {self.fecha_fin}'

# class Ejercicio(models.Model):
#     rutina = models.ForeignKey(RutinaEntrenamiento, on_delete=models.CASCADE, related_name='ejercicios')
#     administrador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ejercicios_creados')
#     nombre = models.CharField(max_length=100)
#     series = models.IntegerField()
#     repeticiones = models.IntegerField()
#     peso_recomendado = models.FloatField()

#     def __str__(self):
#         return str(self.nombre)

# class Ejercicio(models.Model):
#     rutina = models.ForeignKey(RutinaEntrenamiento, on_delete=models.CASCADE, related_name='ejercicios', null=True, blank=True)
#     administrador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ejercicios_creados')
#     nombre = models.CharField(max_length=100)
#     series = models.IntegerField()
#     repeticiones = models.IntegerField()
#     peso_recomendado = models.FloatField()

#     def __str__(self):
#         return str(self.nombre)

# class Ejercicio(models.Model):
#     rutina = models.ForeignKey(RutinaEntrenamiento, on_delete=models.CASCADE, related_name='ejercicios', null=True, blank=True)
#     administrador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ejercicios_creados')
#     nombre = models.CharField(max_length=100)
#     series = models.IntegerField()
#     repeticiones = models.IntegerField()
#     peso_recomendado = models.FloatField()

#     def __str__(self):
#         return str(self.nombre)

class Ejercicio(models.Model):
    rutina = models.ForeignKey(
        'RutinaEntrenamiento', 
        on_delete=models.CASCADE, 
        related_name='ejercicios', 
        null=True, 
        blank=True
    )
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



# class Ejercicio(models.Model):
#     rutina = models.ForeignKey(
#         'RutinaEntrenamiento', 
#         on_delete=models.CASCADE, 
#         related_name='ejercicios', 
#         null=True, 
#         blank=True
#     )
#     administrador = models.ForeignKey(
#         User, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True, 
#         related_name='ejercicios_creados'
#     )
#     nombre = models.CharField(max_length=100)
#     series = models.IntegerField()
#     repeticiones = models.IntegerField()
#     peso_recomendado = models.FloatField()

#     def __str__(self):
#         return str(self.nombre)


class PlanAlimentacion(models.Model):
    cliente = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self): 
        return f'Plan Alimentacion for {self.cliente} from {self.fecha_inicio} to {self.fecha_fin}'

class Comida(models.Model):
    plan = models.ForeignKey(PlanAlimentacion, on_delete=models.CASCADE, related_name='comidas')
    tipo = models.CharField(max_length=50)
    hora = models.TimeField()

    def __str__(self):
        return f'{self.tipo} at {self.hora}'

class Alimento(models.Model):
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE, related_name='alimentos')
    nombre = models.CharField(max_length=100)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre} ({self.cantidad} {self.unidad})'


# MODELO CLIENTE
class ClientePerfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    objetivo = models.CharField(max_length=50, choices=[('fuerza', 'Fuerza'), ('resistencia', 'Resistencia'), ('pérdida de peso', 'Pérdida de peso')], null=True, blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'