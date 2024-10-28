from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SecretKeyForm
from django.contrib.auth import logout as auth_logout
from .models import RutinaEntrenamiento, Ejercicio, PlanAlimentacion, Comida, Alimento
from .forms import RutinaEntrenamientoForm, EjercicioForm, PlanAlimentacionForm, ComidaForm, AlimentoForm
from .models import Ejercicio, PlanAlimentacion, Comida, Alimento
from .forms import EjercicioForm, PlanAlimentacionForm, ComidaForm, AlimentoForm

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
def client_dashboard(request):
    return render(request, 'accounts/client_dashboard.html')

@login_required
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
def admin_dashboard(request):
    # Check if user has validated the secret key
    if not request.session.get('admin_key_validated'):
        return redirect('admin_secret_key')
    return render(request, 'accounts/admin_dashboard.html')

def logout_view(request):
    request.session['admin_key_validated'] = False  # Clear the session variable
    auth_logout(request)
    return redirect('login')
  
  
  
#VIEWS FOR ADMIN MODELS CRUD ACTIONS RUTINA
  
# Rutina Entrenamiento Views
@login_required
def rutina_list(request):
    rutinas = RutinaEntrenamiento.objects.all() # pylint: disable=no-member

    return render(request, 'accounts/rutina_list.html', {'rutinas': rutinas})

@login_required
def rutina_create(request):
    if request.method == 'POST':
        form = RutinaEntrenamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rutina_list')
    else:
        form = RutinaEntrenamientoForm()
    return render(request, 'accounts/rutina_form.html', {'form': form})

@login_required
def rutina_update(request, pk):
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
def rutina_delete(request, pk):
    rutina = get_object_or_404(RutinaEntrenamiento, pk=pk)
    if request.method == 'POST':
        rutina.delete()
        return redirect('rutina_list')
    return render(request, 'accounts/rutina_confirm_delete.html', {'object': rutina})
  

# ejercicio
def ejercicio_list(request):
    ejercicios = Ejercicio.objects.all() #pylint: disable=no-member
    return render(request, 'accounts/ejercicio_list.html', {'ejercicios': ejercicios})

# Create Ejercicio
@login_required
def ejercicio_create(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ejercicio_list')
    else:
        form = EjercicioForm()
    return render(request, 'accounts/ejercicio_form.html', {'form': form})

# Update Ejercicio
@login_required
def ejercicio_update(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            return redirect('ejercicio_list')
    else:
        form = EjercicioForm(instance=ejercicio)
    return render(request, 'accounts/ejercicio_form.html', {'form': form})

# Delete Ejercicio
@login_required
def ejercicio_delete(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        ejercicio.delete()
        return redirect('ejercicio_list')
    return render(request, 'accounts/ejercicio_confirm_delete.html', {'object': ejercicio})
  
# List of PlanAlimentacion
@login_required
def planalimentacion_list(request):
    planes = PlanAlimentacion.objects.all() #pylint: disable=no-member
    return render(request, 'accounts/planalimentacion_list.html', {'planes': planes})

# Create PlanAlimentacion
@login_required
def planalimentacion_create(request):
    if request.method == 'POST':
        form = PlanAlimentacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planalimentacion_list')
    else:
        form = PlanAlimentacionForm()
    return render(request, 'accounts/planalimentacion_form.html', {'form': form})

# Update PlanAlimentacion
@login_required
def planalimentacion_update(request, pk):
    plan = get_object_or_404(PlanAlimentacion, pk=pk)
    if request.method == 'POST':
        form = PlanAlimentacionForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('planalimentacion_list')
    else:
        form = PlanAlimentacionForm(instance=plan)
    return render(request, 'accounts/planalimentacion_form.html', {'form': form})

# Delete PlanAlimentacion
@login_required
def planalimentacion_delete(request, pk):
    plan = get_object_or_404(PlanAlimentacion, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('planalimentacion_list')
    return render(request, 'accounts/planalimentacion_confirm_delete.html', {'object': plan})
  

# List of Comida
@login_required
def comida_list(request):
    comidas = Comida.objects.all() #pylint: disable=no-member
    return render(request, 'accounts/comida_list.html', {'comidas': comidas})

# Create Comida
@login_required
def comida_create(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comida_list')
    else:
        form = ComidaForm()
    return render(request, 'accounts/comida_form.html', {'form': form})

# Update Comida
@login_required
def comida_update(request, pk):
    comida = get_object_or_404(Comida, pk=pk)
    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)
        if form.is_valid():
            form.save()
            return redirect('comida_list')
    else:
        form = ComidaForm(instance=comida)
    return render(request, 'accounts/comida_form.html', {'form': form})

# Delete Comida
@login_required
def comida_delete(request, pk):
    comida = get_object_or_404(Comida, pk=pk)
    if request.method == 'POST':
        comida.delete()
        return redirect('comida_list')
    return render(request, 'accounts/comida_confirm_delete.html', {'object': comida})
  
# List of Alimento
@login_required
def alimento_list(request):
    alimentos = Alimento.objects.all() #pylint: disable=no-member
    return render(request, 'accounts/alimento_list.html', {'alimentos': alimentos})

# Create Alimento
@login_required
def alimento_create(request):
    if request.method == 'POST':
        form = AlimentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alimento_list')
    else:
        form = AlimentoForm()
    return render(request, 'accounts/alimento_form.html', {'form': form})

# Update Alimento
@login_required
def alimento_update(request, pk):
    alimento = get_object_or_404(Alimento, pk=pk)
    if request.method == 'POST':
        form = AlimentoForm(request.POST, instance=alimento)
        if form.is_valid():
            form.save()
            return redirect('alimento_list')
    else:
        form = AlimentoForm(instance=alimento)
    return render(request, 'accounts/alimento_form.html', {'form': form})

# Delete Alimento
@login_required
def alimento_delete(request, pk):
    alimento = get_object_or_404(Alimento, pk=pk)
    if request.method == 'POST':
        alimento.delete()
        return redirect('alimento_list')
    return render(request, 'accounts/alimento_confirm_delete.html', {'object': alimento})