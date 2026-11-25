from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

PERMISOS_POR_GRUPO = {
    "pasajeros": [
        "view_zona", "view_linea", "view_taxisfast",
        "add_viaje", "view_viaje", "change_viaje", "delete_viaje",
    ],
    "choferes": [
        "view_zona", "view_linea", "view_taxisfast", "change_taxisfast",
        "view_viaje", "aceptar_viaje", "completar_viaje",
    ],
    "administradores": None,
}


def crear_grupos(using="default"):
    resumen = {}
    for nombre, codenames in PERMISOS_POR_GRUPO.items():
        permisos = Permission.objects.using(using).filter(content_type__app_label="taxis")
        if codenames is not None:
            permisos = permisos.filter(codename__in=codenames)
        grupo, _ = Group.objects.using(using).get_or_create(name=nombre)
        grupo.permissions.set(permisos)
        resumen[nombre] = permisos.count()

    for usuario in get_user_model().objects.using(using).all():
        usuario.sincronizar_grupo()
    return resumen
