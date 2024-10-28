from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SecretKeyForm
from django.contrib.auth import logout as auth_logout

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