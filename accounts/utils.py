from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from abc import ABC, abstractmethod


# def generar_rutina_personalizada(cliente_perfil):
#     objetivo = cliente_perfil.objetivo
#     ejercicios = Ejercicio.objects.all()  # Todos los ejercicios creados por el superadministrador

#     # Crear o actualizar la rutina
#     rutina, created = RutinaEntrenamiento.objects.get_or_create(
#         cliente=cliente_perfil.usuario,
#         defaults={
#             'fecha_inicio': timezone.now(),
#             'fecha_fin': timezone.now() + timedelta(weeks=4)
#         }
#     )

#     rutina.ejercicios.clear()  # Limpia los ejercicios actuales antes de asignar nuevos

#     if objetivo == 'fuerza':
#         # Ejercicios de alta intensidad
#         ejercicios_filtrados = ejercicios.filter(
#             nombre__icontains='press'
#         ) | ejercicios.filter(nombre__icontains='sentadillas') | ejercicios.filter(nombre__icontains='remo')
#         repeticiones = 6
#         series = 4
#     elif objetivo == 'resistencia':
#         # Ejercicios de moderada intensidad con más repeticiones
#         ejercicios_filtrados = ejercicios.filter(
#             nombre__icontains='fondos'
#         ) | ejercicios.filter(nombre__icontains='zancadas') | ejercicios.filter(nombre__icontains='pull-ups')
#         repeticiones = 15
#         series = 3
#     else:  # Pérdida de peso
#         # Ejercicios de combinación de fuerza y alta intensidad
#         ejercicios_filtrados = ejercicios.filter(
#             nombre__icontains='crunches'
#         ) | ejercicios.filter(nombre__icontains='zancadas') | ejercicios.filter(nombre__icontains='hip thrusts')
#         repeticiones = 12
#         series = 3

#     # Asignar ejercicios con ajustes personalizados
#     for ejercicio in ejercicios_filtrados[:5]:  # Máximo 5 ejercicios
#         rutina.ejercicios.add(ejercicio)
#         ejercicio.series = series
#         ejercicio.repeticiones = repeticiones
#         ejercicio.save()

#     return rutina
def filtrar_ejercicios_por_objetivo(ejercicios, objetivo):
    if objetivo == 'fuerza':
        return ejercicios.filter(
            nombre__icontains='press'
        ) | ejercicios.filter(nombre__icontains='sentadillas') | ejercicios.filter(nombre__icontains='remo'), 6, 4
    elif objetivo == 'resistencia':
        return ejercicios.filter(
            nombre__icontains='fondos'
        ) | ejercicios.filter(nombre__icontains='zancadas') | ejercicios.filter(nombre__icontains='pull-ups'), 15, 3
    else:  # Pérdida de peso
        return ejercicios.filter(
            nombre__icontains='crunches'
        ) | ejercicios.filter(nombre__icontains='zancadas') | ejercicios.filter(nombre__icontains='hip thrusts'), 12, 3

def crear_rutina_base(cliente_perfil):
    rutina, _ = RutinaEntrenamiento.objects.get_or_create(
        cliente=cliente_perfil.usuario,
        defaults={
            'fecha_inicio': timezone.now(),
            'fecha_fin': timezone.now() + timedelta(weeks=4)
        }
    )
    rutina.ejercicios.clear()  # Limpia los ejercicios actuales antes de asignar nuevos
    return rutina

def asignar_ejercicios_a_rutina(rutina, ejercicios_filtrados, series, repeticiones):
    for ejercicio in ejercicios_filtrados[:5]:  # Máximo 5 ejercicios
        rutina.ejercicios.add(ejercicio)
        ejercicio.series = series
        ejercicio.repeticiones = repeticiones
        ejercicio.save()
    return rutina

def generar_rutina_personalizada(cliente_perfil):
    ejercicios = Ejercicio.objects.all()  # Todos los ejercicios creados por el superadministrador
    ejercicios_filtrados, repeticiones, series = filtrar_ejercicios_por_objetivo(ejercicios, cliente_perfil.objetivo)
    rutina = crear_rutina_base(cliente_perfil)
    rutina = asignar_ejercicios_a_rutina(rutina, ejercicios_filtrados, series, repeticiones)
    return rutina

def generar_dieta_personalizada(cliente_perfil):
    peso = cliente_perfil.peso
    altura = cliente_perfil.altura
    objetivo = cliente_perfil.objetivo
    genero = cliente_perfil.genero

    # Cálculo de Metabolismo Basal (MB)
    if genero == 'masculino':
        mb = 66.5 + (13.75 * peso) + (5.003 * altura) - (6.75 * 30)  # Suponiendo edad promedio 30 años
    else:
        mb = 655.1 + (9.563 * peso) + (1.850 * altura) - (4.676 * 30)

    # Cálculo de TDEE y ajuste por objetivo
    tdee = mb * 1.55  # Nivel de actividad moderado por defecto
    if objetivo == 'pérdida de peso':
        tdee *= 0.8  # Reducir 20% calorías
    elif objetivo == 'fuerza':
        tdee *= 1.2  # Incrementar 20% calorías

    # Distribución de macronutrientes
    proteinas_g = 2.2 * peso  # gramos de proteínas
    grasas_g = 1.0 * peso  # gramos de grasas
    carbohidratos_g = (tdee - (proteinas_g * 4 + grasas_g * 9)) / 4  # Resto de calorías en carbohidratos

    # Crear o actualizar el plan de alimentación
    dieta, created = PlanAlimentacion.objects.get_or_create(
        cliente=cliente_perfil.usuario,
        defaults={
            'fecha_inicio': timezone.now(),
            'fecha_fin': timezone.now() + timedelta(weeks=4)
        }
    )

    dieta.comidas.clear()  # Limpia las comidas actuales antes de asignar nuevas

    # Selección de comidas
    comidas = Comida.objects.all()
    comidas_proteinas = comidas.filter(tipo='Proteína')
    comidas_carbohidratos = comidas.filter(tipo='Carbohidrato')
    comidas_grasas = comidas.filter(tipo='Grasas')

    # Función auxiliar para distribuir comidas
    def asignar_comida(tipo_comida, cantidad_requerida):
        # Asignar comidas según el tipo y cantidad requerida
        asignadas = []
        disponibles = comidas.filter(tipo=tipo_comida).order_by('?') 
        for alimento in disponibles:
            if cantidad_requerida <= 0:
                break
            if alimento.cantidad <= cantidad_requerida:
                asignadas.append(alimento)
                cantidad_requerida -= alimento.cantidad
            else:
                # Crear una nueva instancia con la cantidad ajustada
                nueva_comida = Comida(
                    tipo=alimento.tipo,
                    nombre=alimento.nombre,
                    cantidad=cantidad_requerida,
                    unidad=alimento.unidad,
                    hora=alimento.hora
                )
                nueva_comida.save()  # Guardar la comida ajustada
                asignadas.append(nueva_comida)
                cantidad_requerida = 0
        return asignadas

    # Asignar comidas personalizadas
    comidas_asignadas = []
    comidas_asignadas.extend(asignar_comida('Proteína', proteinas_g))
    comidas_asignadas.extend(asignar_comida('Carbohidrato', carbohidratos_g))
    comidas_asignadas.extend(asignar_comida('Grasas', grasas_g))

    # Agregar comidas al plan
    for comida in comidas_asignadas:
        dieta.comidas.add(comida)

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
    
    # Ordenar las comidas por hora
    comidas = dieta.comidas.all().order_by('hora')
    
    # Construir detalles de las comidas
    detalles = [
        {
            'tipo': comida.tipo,
            'hora': comida.hora.strftime('%I:%M %p'),  # Formato legible de hora
            'nombre': comida.nombre,
            'cantidad': comida.cantidad,
            'unidad': comida.unidad
        }
        for comida in comidas
    ]
    
    return {'dieta': dieta, 'detalles': detalles}

# ALGORTIMO DE REPORTE
# def calcular_medias_y_categorizar():
    
#     rutinas = RutinaEntrenamiento.objects.prefetch_related('ejercicios').all()

    
#     total_series = 0
#     total_repeticiones = 0
#     total_ejercicios = 0

#     # Recorrer las rutinas para calcular las sumas totales
#     for rutina in rutinas:
#         for ejercicio in rutina.ejercicios.all():
#             total_series += ejercicio.series
#             total_repeticiones += ejercicio.repeticiones
#             total_ejercicios += 1

#     # Calcular las medias aritméticas
#     media_series = total_series / total_ejercicios if total_ejercicios > 0 else 0
#     media_repeticiones = total_repeticiones / total_ejercicios if total_ejercicios > 0 else 0

#     # Categorizar usuarios que superan las medias
#     usuarios_sobresalientes = []

#     # Sumas totales
#     for rutina in rutinas:
#         usuario = rutina.cliente
#         suma_series_usuario = sum(e.series for e in rutina.ejercicios.all())
#         suma_repeticiones_usuario = sum(e.repeticiones for e in rutina.ejercicios.all())

#         if suma_series_usuario > media_series and suma_repeticiones_usuario > media_repeticiones:
#             usuarios_sobresalientes.append({
#                 'usuario': usuario.username,
#                 'series': suma_series_usuario,
#                 'repeticiones': suma_repeticiones_usuario,
#             })

#     return {
#         'media_series': media_series,
#         'media_repeticiones': media_repeticiones,
#         'usuarios_sobresalientes': usuarios_sobresalientes
#     }

class CalculoEstrategia(ABC):
    @abstractmethod
    def calcular(self, rutinas):
        pass

class MediaSeriesEstrategia(CalculoEstrategia):
    def calcular(self, rutinas):
        total_series = sum(e.series for r in rutinas for e in r.ejercicios.all())
        total_ejercicios = sum(r.ejercicios.count() for r in rutinas)
        return total_series / total_ejercicios if total_ejercicios > 0 else 0

class MediaRepeticionesEstrategia(CalculoEstrategia):
    def calcular(self, rutinas):
        total_repeticiones = sum(e.repeticiones for r in rutinas for e in r.ejercicios.all())
        total_ejercicios = sum(r.ejercicios.count() for r in rutinas)
        return total_repeticiones / total_ejercicios if total_ejercicios > 0 else 0

def calcular_medias_y_categorizar():
    rutinas = RutinaEntrenamiento.objects.prefetch_related('ejercicios').all()
    
    # Usar estrategias para calcular métricas
    media_series = MediaSeriesEstrategia().calcular(rutinas)
    media_repeticiones = MediaRepeticionesEstrategia().calcular(rutinas)

    usuarios_sobresalientes = [
        {
            'usuario': rutina.cliente.username,
            'series': sum(e.series for e in rutina.ejercicios.all()),
            'repeticiones': sum(e.repeticiones for e in rutina.ejercicios.all()),
        }
        for rutina in rutinas
        if sum(e.series for e in rutina.ejercicios.all()) > media_series and
           sum(e.repeticiones for e in rutina.ejercicios.all()) > media_repeticiones
    ]

    return {
        'media_series': media_series,
        'media_repeticiones': media_repeticiones,
        'usuarios_sobresalientes': usuarios_sobresalientes
    }


