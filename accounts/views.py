from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SecretKeyForm
from django.contrib.auth import logout as auth_logout
from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida
from .forms import RutinaEntrenamientoForm, EjercicioForm, PlanAlimentacionForm, ComidaForm
from .models import Ejercicio, PlanAlimentacion, Comida
from .forms import EjercicioForm, PlanAlimentacionForm, ComidaForm
from .forms import ClientePerfilForm
from .utils import generar_rutina_personalizada, generar_dieta_personalizada, obtener_rutina, obtener_dieta
from .models import ClientePerfil  # Agrega esta línea
from .decorators import superadmin_required


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        # Si ya hay un usuario autenticado, cerrar la sesión actual
        if request.user.is_authenticated:
            auth_logout(request)

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('choose_role')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def choose_role(request):
    return render(request, 'accounts/choose_role.html')
  

@login_required
@superadmin_required 
def admin_secret_key(request):
    if request.method == 'POST':
        form = SecretKeyForm(request.POST)
        if form.is_valid():
            # Store validation status in the session
            request.session['admin_key_validated'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Incorrect secret key. Please try again.")
    else:
        form = SecretKeyForm()
    return render(request, 'accounts/admin_secret_key.html', {'form': form})

@login_required
@superadmin_required
def admin_dashboard(request):
    # Check if user has validated the secret key
    if not request.session.get('admin_key_validated'):
        return redirect('admin_secret_key')
    return render(request, 'accounts/admin_dashboard.html')

def logout_view(request):
    request.session['admin_key_validated'] = False  # Clear the session variable
    auth_logout(request)
    return redirect('login')

@login_required
@superadmin_required 
def create_rutina(request):
    if request.method == 'POST':
        form = RutinaEntrenamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rutina_list')
    else:
        form = RutinaEntrenamientoForm()
    return render(request, 'accounts/rutina_form.html', {'form': form})

@login_required
@superadmin_required 
def create_ejercicio(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ejercicio_list')
    else:
        form = EjercicioForm()
    return render(request, 'accounts/ejercicio_form.html', {'form': form})

def create_planalimentacion(request):
    if request.method == 'POST':
        form = PlanAlimentacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planalimentacion_list')
    else:
        form = PlanAlimentacionForm()
    return render(request, 'accounts/planalimentacion_form.html', {'form': form})

def create_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comida_list')
    else:
        form = ComidaForm()
    return render(request, 'accounts/comida_form.html', {'form': form})
 
  
#demas metodos
# List views
@login_required
def rutina_list(request):
    rutinas = RutinaEntrenamiento.objects.all()
    return render(request, 'accounts/rutina_list.html', {'rutinas': rutinas})

def ejercicio_list(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'accounts/ejercicio_list.html', {'ejercicios': ejercicios})

def planalimentacion_list(request):
    planes = PlanAlimentacion.objects.all()
    return render(request, 'accounts/planalimentacion_list.html', {'planes': planes})

@login_required
@superadmin_required 
def comida_list(request):
    comidas = Comida.objects.all()
    return render(request, 'accounts/comida_list.html', {'comidas': comidas})


# Update views
@login_required
@superadmin_required 
def update_rutina(request, pk):
    rutina = get_object_or_404(RutinaEntrenamiento, pk=pk)
    if request.method == 'POST':
        form = RutinaEntrenamientoForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            return redirect('rutina_list')
    else:
        form = RutinaEntrenamientoForm(instance=rutina)
    return render(request, 'accounts/rutina_form.html', {'form': form})

@login_required
@superadmin_required 
def update_ejercicio(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            return redirect('ejercicio_list')
    else:
        form = EjercicioForm(instance=ejercicio)
    return render(request, 'accounts/ejercicio_form.html', {'form': form})

@login_required
@superadmin_required 
def update_planalimentacion(request, pk):
    plan = get_object_or_404(PlanAlimentacion, pk=pk)
    if request.method == 'POST':
        form = PlanAlimentacionForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('planalimentacion_list')
    else:
        form = PlanAlimentacionForm(instance=plan)
    return render(request, 'accounts/planalimentacion_form.html', {'form': form})

@login_required
@superadmin_required 
def update_comida(request, pk):
    comida = get_object_or_404(Comida, pk=pk)
    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)
        if form.is_valid():
            form.save()
            return redirect('comida_list')
    else:
        form = ComidaForm(instance=comida)
    return render(request, 'accounts/comida_form.html', {'form': form})


# Delete views
@login_required
@superadmin_required 
def delete_rutina(request, pk):
    rutina = get_object_or_404(RutinaEntrenamiento, pk=pk)
    if request.method == 'POST':
        rutina.delete()
        return redirect('rutina_list')
    return render(request, 'accounts/rutina_confirm_delete.html', {'rutina': rutina})

@login_required
@superadmin_required 
def delete_ejercicio(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        ejercicio.delete()
        return redirect('ejercicio_list')
    return render(request, 'accounts/ejercicio_confirm_delete.html', {'ejercicio': ejercicio})

@login_required
@superadmin_required 
def delete_planalimentacion(request, pk):
    plan = get_object_or_404(PlanAlimentacion, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('planalimentacion_list')
    return render(request, 'accounts/planalimentacion_confirm_delete.html', {'plan': plan})

@login_required
@superadmin_required 
def delete_comida(request, pk):
    comida = get_object_or_404(Comida, pk=pk)
    if request.method == 'POST':
        comida.delete()
        return redirect('comida_list')
    return render(request, 'accounts/comida_confirm_delete.html', {'comida': comida})


@login_required
def client_dashboard(request):
    perfil = request.user.perfil  # Obtiene el perfil del cliente
    rutina = obtener_rutina(perfil)
    dieta = obtener_dieta(perfil)
    return render(request, 'accounts/client_dashboard.html', {'perfil': perfil, 'rutina': rutina, 'dieta': dieta})

@login_required
def actualizar_perfil(request):
    perfil, created = ClientePerfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = ClientePerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            generar_rutina_personalizada(perfil)
            generar_dieta_personalizada(perfil)
            return redirect('client_dashboard')
    else:
        form = ClientePerfilForm(instance=perfil)
    return render(request, 'accounts/actualizar_perfil.html', {'form': form})


