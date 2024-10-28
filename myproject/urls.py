"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('choose_role/', account_views.choose_role, name='choose_role'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('client_dashboard/', account_views.client_dashboard, name='client_dashboard'),
    path('admin_dashboard/', account_views.admin_dashboard, name='admin_dashboard'),
    
    path('admin_secret_key/', account_views.admin_secret_key, name='admin_secret_key'),
    path('admin_dashboard/', account_views.admin_dashboard, name='admin_dashboard'),
    
    path('logout/', account_views.logout_view, name='logout'),
    
    path('rutinas/', views.rutina_list, name='rutina_list'),
    path('rutina/create/', views.rutina_create, name='rutina_create'),
    path('rutina/<int:pk>/update/', views.rutina_update, name='rutina_update'),
    path('rutina/<int:pk>/delete/', views.rutina_delete, name='rutina_delete'),
    
    # Ejercicio URLs
    path('ejercicios/', views.ejercicio_list, name='ejercicio_list'),
    path('ejercicio/create/', views.ejercicio_create, name='ejercicio_create'),
    path('ejercicio/<int:pk>/update/', views.ejercicio_update, name='ejercicio_update'),
    path('ejercicio/<int:pk>/delete/', views.ejercicio_delete, name='ejercicio_delete'),

    # PlanAlimentacion URLs
    path('planes/', views.planalimentacion_list, name='planalimentacion_list'),
    path('plan/create/', views.planalimentacion_create, name='planalimentacion_create'),
    path('plan/<int:pk>/update/', views.planalimentacion_update, name='planalimentacion_update'),
    path('plan/<int:pk>/delete/', views.planalimentacion_delete, name='planalimentacion_delete'),

    # Comida URLs
    path('comidas/', views.comida_list, name='comida_list'),
    path('comida/create/', views.comida_create, name='comida_create'),
    path('comida/<int:pk>/update/', views.comida_update, name='comida_update'),
    path('comida/<int:pk>/delete/', views.comida_delete, name='comida_delete'),

    # Alimento URLs
    path('alimentos/', views.alimento_list, name='alimento_list'),
    path('alimento/create/', views.alimento_create, name='alimento_create'),
    path('alimento/<int:pk>/update/', views.alimento_update, name='alimento_update'),
    path('alimento/<int:pk>/delete/', views.alimento_delete, name='alimento_delete'),

]
