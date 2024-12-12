# Gym Tracking App

## Descripción
Esta aplicación está diseñada para gestionar las necesidades de un gimnasio, ofreciendo funcionalidades tanto para administradores como para clientes. Proporciona una solución integral que incluye la creación y personalización de rutinas de ejercicios y planes de alimentación basados en los objetivos y características de cada cliente.

## Características Principales

### Lado Administrador o Superadministrador
- **Gestión de ejercicios:**
  - Crear y actualizar la lista de ejercicios disponibles.
  - Detallar series, repeticiones y peso recomendado para cada ejercicio.
  
  **Ejemplo de ejercicios:**
  | Nombre             | Series | Repeticiones | Peso Recomendado |
  |--------------------|--------|--------------|------------------|
  | Pecho (press)      | 4      | 2            | 30.0 kg          |
  | Brazos (bíceps)    | 3      | 10           | 12.0 kg          |

- **Gestión de comidas:**
  - Crear y actualizar la lista de alimentos y sus respectivas cantidades.
  - Establecer horarios para cada tipo de comida (proteína, carbohidrato, grasas, etc.).
  
  **Ejemplo de comidas:**
  | Tipo         | Hora     | Nombre           | Cantidad | Unidad  |
  |--------------|----------|------------------|----------|---------|
  | Proteína     | 7:30 a.m.| Pollo (pechuga)  | 199.0    | gramos  |
  | Carbohidrato | 8:00 a.m.| Arroz integral   | 150.0    | gramos  |

- **Supervisión personalizada:**
  - Visualizar las rutinas y planes alimenticios existentes asignados a cada cliente.
  
  **Ejemplo de rutinas asignadas:**
  | Cliente | Fecha de Inicio | Fecha de Fin |
  |---------|-----------------|--------------|
  | Andrés  | Dec 09, 2024    | Jan 06, 2025 |

  **Detalles de ejercicios asignados:**
  - Abdominales (crunches): Series: 3, Repeticiones: 12, Peso: 0.0 kg
  - Glúteos (zancadas): Series: 3, Repeticiones: 12, Peso: 10.0 kg
  - Glúteos (hip thrusts): Series: 3, Repeticiones: 12, Peso: 40.0 kg

  **Ejemplo de planes alimenticios asignados:**
  | Cliente | Fecha de Inicio | Fecha de Fin |
  |---------|-----------------|--------------|
  | Andrés  | Dec 09, 2024    | Jan 06, 2025 |

  **Detalles de comidas asignadas:**
  - Proteína: Huevos (enteros), Cantidad: 3.0 unidades, Hora: 8:30 a.m.
  - Grasas: Almendras, Cantidad: 20.0 gramos, Hora: 8:00 p.m.
  - Carbohidrato: Avena, Cantidad: 40.0 gramos, Hora: 4:30 p.m.

### Lado Cliente
- **Perfil Personalizado:**
  - Registro de datos iniciales: peso, altura y objetivo (fuerza, resistencia, pérdida de peso).
  - Actualización de datos personales.
- **Rutina y dieta personalizada:**
  - Generación automática de rutinas de ejercicios y planes de alimentación adaptados a las metas del cliente.

## Estructura del Proyecto
- **Cliente:** Interfaz que permite a los usuarios ingresar y actualizar su información, y acceder a su rutina y dieta personalizadas.
- **Administrador:** Herramienta para gestionar ejercicios, comidas y supervisar planes personalizados de los clientes.

## Requisitos del Sistema
- **Backend:** Python, django framework, javascript.
- **Frontend:** HTML 5, CSS 3, Tailwind CSS.
- **Base de datos:** Sqlite.
- **Dependencias:**
  - Django==5.1.1
  - gunicorn==23.0.0

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/andresguaman0621/gym_project.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd gym_project
   ```
3. Instala las dependencias del backend:
   ```bash
   pip install -r requirements.txt
   ```
   
## Uso
1. Iniciar la ejecución:
   ```bash
   python manage.py runserver
   ```
3. Accede a la aplicación en tu navegador:
   - Cliente/Administrador: `http://localhost:8000`


## Licencia
Este proyecto está licenciado bajo la [MIT License](LICENSE).

