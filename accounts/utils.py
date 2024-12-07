from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida, Alimento
from datetime import timedelta
from django.utils import timezone

def generar_rutina_personalizada(cliente_perfil):
    objetivo = cliente_perfil.objetivo
    ejercicios = Ejercicio.objects.filter(administrador__isnull=False, rutina__isnull=True)  # Ejercicios globales

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

    for ejercicio in ejercicios_filtrados[:5]:
        rutina.ejercicios.create(
            nombre=ejercicio.nombre,
            series=3,
            repeticiones=10,
            peso_recomendado=20 if objetivo == 'fuerza' else 0
        )
    return rutina


def generar_dieta_personalizada(cliente_perfil):
    peso = cliente_perfil.peso
    objetivo = cliente_perfil.objetivo

    dieta = PlanAlimentacion.objects.filter(cliente=cliente_perfil.usuario).first()
    if not dieta:
        dieta = PlanAlimentacion.objects.create(
            cliente=cliente_perfil.usuario,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(weeks=4)
        )

    comidas = Comida.objects.filter(plan=dieta)
    if not comidas.exists():
        tipos_comidas = ['Desayuno', 'Almuerzo', 'Cena']
        for tipo in tipos_comidas:
            comida = Comida.objects.create(plan=dieta, tipo=tipo, hora='08:00' if tipo == 'Desayuno' else '12:00' if tipo == 'Almuerzo' else '19:00')
            Alimento.objects.create(comida=comida, nombre='Arroz', cantidad=100, unidad='g')
            Alimento.objects.create(comida=comida, nombre='Pollo', cantidad=150, unidad='g')
            Alimento.objects.create(comida=comida, nombre='Verduras', cantidad=100, unidad='g')

    return dieta



def obtener_rutina(cliente_perfil):
    rutina = RutinaEntrenamiento.objects.filter(cliente=cliente_perfil.usuario).order_by('-fecha_inicio').first()
    if not rutina:
        return None  # Si no hay rutina, devuelve None
    ejercicios = rutina.ejercicios.all()
    return {'rutina': rutina, 'ejercicios': ejercicios}

def obtener_dieta(cliente_perfil):
    dieta = PlanAlimentacion.objects.filter(cliente=cliente_perfil.usuario).order_by('-fecha_inicio').first()
    if not dieta:
        return None  # Si no hay dieta, devuelve None
    comidas = dieta.comidas.all()
    detalles = []
    for comida in comidas:
        alimentos = comida.alimentos.all()
        detalles.append({'comida': comida, 'alimentos': alimentos})
    return {'dieta': dieta, 'detalles': detalles}
