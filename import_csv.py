import os
import csv
import django

# Configuración para cargar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Reemplaza 'myproject' con el nombre de tu proyecto
django.setup()

from accounts.models import Ejercicio, Comida

# Obtén la ruta del directorio donde se encuentra el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def importar_csv(ruta_csv, modelo, campos):
    with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            datos = {campo: fila[campo] for campo in campos}
            modelo.objects.get_or_create(**datos)

def run():
    # Importar ejercicios
    importar_csv(
        ruta_csv=os.path.join(BASE_DIR, 'ejercicios.csv'),  # Ruta absoluta del archivo CSV
        modelo=Ejercicio,
        campos=["nombre", "series", "repeticiones", "peso_recomendado"]
    )

    # Importar comidas
    importar_csv(
        ruta_csv=os.path.join(BASE_DIR, 'comidas.csv'),  # Ruta absoluta del archivo CSV
        modelo=Comida,
        campos=["tipo", "hora", "nombre", "cantidad", "unidad"]
    )

    print("Datos importados correctamente.")

if __name__ == '__main__':
    run()
