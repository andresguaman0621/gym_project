from django.db import models

class RutinaEntrenamiento(models.Model):
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    def __str__(self):
        return f"Rutina del {self.fechaInicio} al {self.fechaFin}"

class Ejercicio(models.Model):
    rutina = models.ForeignKey(RutinaEntrenamiento, related_name="ejercicios", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    pesoRecomendado = models.FloatField()

    def __str__(self):
        return str(self.nombre)

class PlanAlimentacion(models.Model):
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    def __str__(self):
        return f"Plan del {self.fechaInicio} al {self.fechaFin}"

class Comida(models.Model):
    plan = models.ForeignKey(PlanAlimentacion, related_name="comidas", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # E.g., desayuno, almuerzo
    hora = models.TimeField()

    def __str__(self):
        return f"{self.tipo} a las {self.hora}"

class Alimento(models.Model):
    comida = models.ForeignKey(Comida, related_name="alimentos", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=20)  # E.g., gramos, mililitros

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.nombre}"
