from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminPagesMiddleware:
    """
    Middleware para restringir páginas de administrador solo al superadministrador.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de rutas restringidas
        admin_pages = [
            reverse('admin_secret_key'),
            reverse('admin_dashboard'),
        ]

        # Verificar si el usuario intenta acceder a una página restringida
        if request.path in admin_pages:
            if not request.user.is_authenticated or not request.user.is_superuser:
                return redirect('login')  # Redirigir al login si no es superadmin

        response = self.get_response(request)
        return response
