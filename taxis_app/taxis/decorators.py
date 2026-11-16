from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def rol_requerido(*roles):
    """Deja pasar solo a usuarios con sesión iniciada Y con alguno de los roles dados.

    - Sin sesión: lo manda a iniciar sesión (y vuelve a la página que quería).
    - Con otro rol: aviso y lo regresa a su propio panel.
    """

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
