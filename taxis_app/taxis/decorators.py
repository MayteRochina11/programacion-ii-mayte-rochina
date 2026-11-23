from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def rol_requerido(*roles):

    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.rol not in roles:
                messages.error(request, "No tienes permiso para entrar a esa página.")
                return redirect("inicio")
            return vista(request, *args, **kwargs)

        return envoltura

    return decorador
