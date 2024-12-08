from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida
from datetime import timedelta
from django.utils import timezone


def generar_rutina_personalizada(cliente_perfil):
    objetivo = cliente_perfil.objetivo
    ejercicios = Ejercicio.objects.all()  # Todos los ejercicios creados por el superadministrador

    rutina = RutinaEntrenamiento.objects.filter(cliente=cliente_perfil.usuario).first()
    if not rutina:
        rutina = RutinaEntrenamiento.objects.create(
            cliente=cliente_perfil.usuario,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(weeks=4)
        )

    if objetivo == 'fuerza':
        ejercicios_filtrados = ejercicios.filter(nombre__icontains='peso')
    elif objetivo == 'resistencia':
        ejercicios_filtrados = ejercicios.filter(nombre__icontains='cardio')
    else:  # Pérdida de peso
        ejercicios_filtrados = ejercicios.filter(nombre__icontains='calistenia')

    rutina.ejercicios.clear()  # Limpia los ejercicios existentes antes de agregar nuevos
    for ejercicio in ejercicios_filtrados[:5]:  # Toma hasta 5 ejercicios
        rutina.ejercicios.create(
            nombre=ejercicio.nombre,
            series=ejercicio.series,
            repeticiones=ejercicio.repeticiones,
            peso_recomendado=ejercicio.peso_recomendado
        )
    return rutina


def generar_dieta_personalizada(cliente_perfil):
    dieta = PlanAlimentacion.objects.filter(cliente=cliente_perfil.usuario).first()
    if not dieta:
        dieta = PlanAlimentacion.objects.create(
            cliente=cliente_perfil.usuario,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(weeks=4)
        )

    dieta.comidas.clear()  # Limpia las comidas existentes antes de agregar nuevas
    comidas = Comida.objects.all()  # Todas las comidas creadas por el superadministrador
    tipos_comidas = ['Desayuno', 'Almuerzo', 'Cena']

    for tipo in tipos_comidas:
        comidas_tipo = comidas.filter(tipo=tipo)
        if comidas_tipo.exists():
            comida = comidas_tipo.first()  # Selecciona una comida del catálogo
            dieta.comidas.create(
                tipo=comida.tipo,
                hora=comida.hora,
                nombre=comida.nombre,
                cantidad=comida.cantidad,
                unidad=comida.unidad
            )
    return dieta



def obtener_rutina(cliente_perfil):
    rutina = RutinaEntrenamiento.objects.filter(cliente=cliente_perfil.usuario).order_by('-fecha_inicio').first()
    if not rutina:
        return None  # Si no hay rutina, devuelve None
    ejercicios = rutina.ejercicios.all()  # Ahora obtenemos los ejercicios asignados
    return {'rutina': rutina, 'ejercicios': ejercicios}


def generar_dieta_personalizada(cliente_perfil):
    dieta, created = PlanAlimentacion.objects.get_or_create(
        cliente=cliente_perfil.usuario,
        fecha_inicio=timezone.now(),
        fecha_fin=timezone.now() + timedelta(weeks=4)
    )

    dieta.comidas.clear()  # Limpia las comidas actuales asociadas al plan
    comidas = Comida.objects.all()  # Todas las comidas creadas por el superadministrador
    tipos_comidas = ['Desayuno', 'Almuerzo', 'Cena']

    for tipo in tipos_comidas:
        comidas_tipo = comidas.filter(tipo=tipo)
        if comidas_tipo.exists():
            comida = comidas_tipo.first()  # Selecciona una comida del catálogo
            dieta.comidas.add(comida)  # Asocia la comida al plan

    return dieta


def obtener_dieta(cliente_perfil):
    # Obtiene la dieta más reciente asociada al cliente
    dieta = PlanAlimentacion.objects.filter(cliente=cliente_perfil.usuario).order_by('-fecha_inicio').first()
    if not dieta:
        return None  # Si no hay dieta, devuelve None
    
    # Obtiene todas las comidas asociadas al plan de alimentación
    comidas = dieta.comidas.all()
    detalles = []

    # Construye los detalles directamente desde las comidas
    for comida in comidas:
        detalles.append({
            'tipo': comida.tipo,
            'hora': comida.hora,
            'nombre': comida.nombre,
            'cantidad': comida.cantidad,
            'unidad': comida.unidad,
        })
    
    # Retorna la dieta con sus detalles
    return {
        'dieta': dieta,
        'detalles': detalles,
    }
