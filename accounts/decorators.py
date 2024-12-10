from django.shortcuts import redirect
from functools import wraps

def superadmin_required(view_func):
    
    # Decorador personalizado para restringir vistas solo al superadministrador
    
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('login')  # Redirige al login si no es superadmin
        return view_func(request, *args, **kwargs)
    return _wrapped_view
