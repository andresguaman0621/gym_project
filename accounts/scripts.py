from accounts.models import Ejercicio, ClientePerfil, PlanAlimentacion, RutinaEntrenamiento

# Consultar todos los ejercicios
def consultar_ejercicios():
    ejercicios = Ejercicio.objects.all()
    for ejercicio in ejercicios:
        print(f"ID: {ejercicio.id}, Nombre: {ejercicio.nombre}, Series: {ejercicio.series}, Repeticiones: {ejercicio.repeticiones}, Peso: {ejercicio.peso_recomendado} kg")

# Consultar perfiles de clientes
def consultar_clientes():
    clientes = ClientePerfil.objects.all()
    for cliente in clientes:
        print(f"Username: {cliente.usuario.username}, Peso: {cliente.peso}, Altura: {cliente.altura}, Objetivo: {cliente.objetivo}")

# Consultar rutinas asignadas
def consultar_rutinas():
    rutinas = RutinaEntrenamiento.objects.all()
    for rutina in rutinas:
        print(f"Cliente: {rutina.cliente.username}, Inicio: {rutina.fecha_inicio}, Fin: {rutina.fecha_fin}")
        for ejercicio in rutina.ejercicios.all():
            print(f"  - Ejercicio: {ejercicio.nombre}, Series: {ejercicio.series}, Repeticiones: {ejercicio.repeticiones}")

# Consultar planes de alimentación asignados
def consultar_planes_alimentacion():
    planes = PlanAlimentacion.objects.all()
    for plan in planes:
        print(f"Cliente: {plan.cliente.username}, Inicio: {plan.fecha_inicio}, Fin: {plan.fecha_fin}")
        for comida in plan.comidas.all():
            print(f"  - Comida: {comida.nombre}, Tipo: {comida.tipo}, Cantidad: {comida.cantidad} {comida.unidad}")
