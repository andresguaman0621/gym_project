# accounts/models.py

from django.db import models

class RutinaEntrenamiento(models.Model):
    cliente = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming cliente is a user
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f'Rutina for {self.cliente} from {self.fecha_inicio} to {self.fecha_fin}'

class Ejercicio(models.Model):
    rutina = models.ForeignKey(RutinaEntrenamiento, on_delete=models.CASCADE, related_name='ejercicios')
    nombre = models.CharField(max_length=100)
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    peso_recomendado = models.FloatField()

    def __str__(self):
        return str(self.nombre)

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
