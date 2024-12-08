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
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redirige la raíz a login/
    
    path('admin/', admin.site.urls),
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('choose_role/', account_views.choose_role, name='choose_role'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # path('client_dashboard/', account_views.client_dashboard, name='client_dashboard'),
    path('admin_dashboard/', account_views.admin_dashboard, name='admin_dashboard'),
    
    path('admin_secret_key/', account_views.admin_secret_key, name='admin_secret_key'),
    path('admin_dashboard/', account_views.admin_dashboard, name='admin_dashboard'),
    
    path('logout/', account_views.logout_view, name='logout'),
    
    # List views
    path('rutinas/', views.rutina_list, name='rutina_list'),
    path('ejercicios/', views.ejercicio_list, name='ejercicio_list'),
    path('planes_alimentacion/', views.planalimentacion_list, name='planalimentacion_list'),
    path('comidas/', views.comida_list, name='comida_list'),
    

    # Create views
    path('rutina/create/', views.create_rutina, name='create_rutina'),
    path('ejercicio/create/', views.create_ejercicio, name='create_ejercicio'),
    path('planalimentacion/create/', views.create_planalimentacion, name='create_planalimentacion'),
    path('comida/create/', views.create_comida, name='create_comida'),
    

    # Update views
    path('rutina/update/<int:pk>/', views.update_rutina, name='update_rutina'),
    path('ejercicio/update/<int:pk>/', views.update_ejercicio, name='update_ejercicio'),
    path('planalimentacion/update/<int:pk>/', views.update_planalimentacion, name='update_planalimentacion'),
    path('comida/update/<int:pk>/', views.update_comida, name='update_comida'),
    
    
    # Delete views
    path('rutina/delete/<int:pk>', views.delete_rutina, name='delete_rutina'),
    path('ejercicio/delete/<int:pk>', views.delete_ejercicio, name='delete_ejercicio'),
    path('planalimentacion/delete/<int:pk>', views.delete_planalimentacion, name='delete_planalimentacion'),
    path('comida/delete/<int:pk>', views.delete_comida, name='delete_comida'),
    
        
        
    # RUTAS CLIENTES
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    # path('registro/', views.registro_cliente, name='registro_cliente'),
]
