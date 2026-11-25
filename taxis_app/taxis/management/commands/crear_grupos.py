from django.core.management.base import BaseCommand

from taxis.grupos import crear_grupos


class Command(BaseCommand):
    help = "Crea los grupos pasajeros, choferes y administradores con sus permisos."

    def handle(self, *args, **options):
        for nombre, total in crear_grupos().items():
            self.stdout.write(self.style.SUCCESS(f"Grupo '{nombre}': {total} permisos"))
