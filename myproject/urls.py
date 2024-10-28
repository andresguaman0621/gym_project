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

]
