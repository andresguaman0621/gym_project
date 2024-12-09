from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida
from datetime import timedelta
from django.utils import timezone


def generar_rutina_personalizada(cliente_perfil):
    objetivo = cliente_perfil.objetivo
    ejercicios = Ejercicio.objects.all()  # Todos los ejercicios creados por el superadministrador

    rutina, created = RutinaEntrenamiento.objects.get_or_create(
        cliente=cliente_perfil.usuario,
        fecha_inicio=timezone.now(),
        fecha_fin=timezone.now() + timedelta(weeks=4)
    )

    rutina.ejercicios.clear()  # Limpia los ejercicios actuales antes de asignar nuevos

    if objetivo == 'fuerza':
        ejercicios_filtrados = ejercicios.filter(nombre__icontains='espalda')
    elif objetivo == 'resistencia':
        ejercicios_filtrados = ejercicios.filter(nombre__icontains='piernas')
    else:  # Pérdida de peso
        ejercicios_filtrados = ejercicios.filter(nombre__icontains='brazos')

    rutina.ejercicios.add(*ejercicios_filtrados[:5])  # Asigna hasta 5 ejercicios filtrados
    return rutina

def generar_dieta_personalizada(cliente_perfil):
    dieta, created = PlanAlimentacion.objects.get_or_create(
        cliente=cliente_perfil.usuario,
        fecha_inicio=timezone.now(),
        fecha_fin=timezone.now() + timedelta(weeks=4)
    )

    dieta.comidas.clear()  # Limpia las comidas actuales antes de asignar nuevas

    comidas = Comida.objects.all()  # Todas las comidas creadas por el superadministrador
    tipos_comidas = ['proteina', 'carbohidrato','grasas']

    for tipo in tipos_comidas:
        comidas_tipo = comidas.filter(tipo=tipo)
        if comidas_tipo.exists():
            comida = comidas_tipo.first()  # Selecciona una comida relevante del catálogo
            dieta.comidas.add(comida)  # Asocia la comida al plan

    return dieta

def obtener_rutina(cliente_perfil):
    rutina = RutinaEntrenamiento.objects.filter(cliente=cliente_perfil.usuario).order_by('-fecha_inicio').first()
    if not rutina:
        return None
    ejercicios = rutina.ejercicios.all()
    return {'rutina': rutina, 'ejercicios': ejercicios}

def obtener_dieta(cliente_perfil):
    dieta = PlanAlimentacion.objects.filter(cliente=cliente_perfil.usuario).order_by('-fecha_inicio').first()
    if not dieta:
        return None
    comidas = dieta.comidas.all()
    detalles = [{'tipo': comida.tipo, 'hora': comida.hora, 'nombre': comida.nombre, 'cantidad': comida.cantidad, 'unidad': comida.unidad} for comida in comidas]
    return {'dieta': dieta, 'detalles': detalles}
