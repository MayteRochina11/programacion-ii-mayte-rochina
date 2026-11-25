from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from taxis.grupos import crear_grupos
from taxis.models import Linea, TaxisFast, Usuario, Viaje, Zona

CLAVE_ADMIN = "Admin2026*"
CLAVE_USUARIOS = "Taxis2026*"

ZONAS = [
    ("Centro Histórico", "Casco colonial y plazas principales"),
    ("La Mariscal", "Zona turística y de oficinas"),
    ("Quitumbe", "Sur de la ciudad, terminal terrestre"),
    ("Cumbayá", "Valle oriental, universidades"),
    ("Carcelén", "Norte de la ciudad"),
    ("Aeropuerto", "Parroquia de Tababela y vías de acceso"),
]

LINEAS = [
    ("Línea Centro", "Centro", ["Centro Histórico", "La Mariscal"]),
    ("Línea Norte", "Norte", ["Carcelén", "La Mariscal"]),
    ("Línea Sur", "Sur", ["Quitumbe", "Centro Histórico"]),
    ("Línea Valles", "Valles", ["Cumbayá", "Aeropuerto"]),
    ("Línea Aeropuerto", "Aeropuerto", ["Aeropuerto", "Cumbayá", "La Mariscal"]),
]

CHOFERES = [
    ("chofer1", "Carlos", "Andrade", "Amarillo 1", "PBA-1001", "1.50", "Línea Centro", "EN_BASE"),
    ("chofer2", "Luis", "Mena", "Rayo 2", "PBA-1002", "1.75", "Línea Norte", "EN_SERVICIO"),
    ("chofer3", "Marco", "Paredes", "Halcón 3", "PBA-1003", "1.25", "Línea Sur", "EN_BASE"),
    ("chofer4", "Diego", "Salazar", "Estrella 4", "PBA-1004", "2.00", "Línea Valles", "EN_BASE"),
    ("chofer5", "Jorge", "Vera", "Veloz 5", "PBA-1005", "1.60", "Línea Aeropuerto", "FUERA_DE_SERVICIO"),
]

PASAJEROS = [
    ("pasajero1", "Ana", "Torres"),
    ("pasajero2", "Lucía", "Mora"),
    ("pasajero3", "Pedro", "Ruiz"),
    ("pasajero4", "Sofía", "Vega"),
    ("pasajero5", "Mateo", "Cruz"),
]

VIAJES = [
    ("pasajero1", "Parque La Carolina", "Aeropuerto Mariscal Sucre", None, "PENDIENTE"),
    ("pasajero2", "Plaza Grande", "Terminal Quitumbe", None, "PENDIENTE"),
    ("pasajero3", "Quicentro Norte", "Cumbayá", None, "PENDIENTE"),
    ("pasajero4", "Universidad UTE", "La Mariscal", "chofer2", "ASIGNADO"),
    ("pasajero5", "Terminal Quitumbe", "Centro Histórico", "chofer1", "COMPLETADO"),
    ("pasajero1", "Cumbayá", "Parque La Carolina", "chofer3", "COMPLETADO"),
    ("pasajero2", "La Mariscal", "Carcelén", "chofer1", "COMPLETADO"),
]


class Command(BaseCommand):
    help = "Carga datos de prueba (5+ registros por tabla y usuarios de cada grupo). Se puede repetir."

    @transaction.atomic
    def handle(self, *args, **options):
        crear_grupos()

        admin = Usuario.objects.filter(username="admin").first()
        if admin is None and not Usuario.objects.filter(rol=Usuario.Rol.ADMIN).exists():
            Usuario.objects.create_superuser("admin", "admin@taxisfast.test", CLAVE_ADMIN,
                                             first_name="Administrador", last_name="TaxisFast")
            self.stdout.write("Administrador 'admin' creado.")
        elif admin is not None and admin.rol == Usuario.Rol.ADMIN:
            admin.set_password(CLAVE_ADMIN)
            admin.save()
            self.stdout.write("Administrador 'admin' ya existía: contraseña restablecida.")
        else:
            self.stdout.write(self.style.WARNING(
                "Ya existe otro administrador; no se crea 'admin' (solo puede haber uno)."))

        zonas = {}
        for nombre, descripcion in ZONAS:
            zonas[nombre], _ = Zona.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})
        lineas = {}
        for nombre, zona_texto, cubre in LINEAS:
            linea, _ = Linea.objects.get_or_create(nombre=nombre, defaults={"zona": zona_texto})
            linea.zonas.set([zonas[z] for z in cubre])
            lineas[nombre] = linea

        choferes = {}
        for usuario, nombre, apellido, taxi, placa, tarifa, linea, estado in CHOFERES:
            chofer, creado = Usuario.objects.get_or_create(username=usuario, defaults={
                "first_name": nombre, "last_name": apellido, "rol": Usuario.Rol.CHOFER,
                "email": f"{usuario}@taxisfast.test", "telefono": f"099100000{usuario[-1]}",
            })
            if creado:
                chofer.set_password(CLAVE_USUARIOS)
                chofer.save()
            TaxisFast.objects.get_or_create(chofer=chofer, defaults={
                "taxi": taxi, "taxi_placa": placa, "taxi_tarifa": Decimal(tarifa),
                "linea": lineas[linea], "estado": estado,
            })
            choferes[usuario] = chofer

        pasajeros = {}
        for usuario, nombre, apellido in PASAJEROS:
            pasajero, creado = Usuario.objects.get_or_create(username=usuario, defaults={
                "first_name": nombre, "last_name": apellido, "rol": Usuario.Rol.PASAJERO,
                "email": f"{usuario}@taxisfast.test", "telefono": f"098200000{usuario[-1]}",
            })
            if creado:
                pasajero.set_password(CLAVE_USUARIOS)
                pasajero.save()
            pasajeros[usuario] = pasajero

        for usuario, origen, destino, chofer, estado in VIAJES:
            taxi = choferes[chofer].vehiculo if chofer else None
            Viaje.objects.get_or_create(
                creado_por=pasajeros[usuario], origen=origen, destino=destino,
                defaults={"taxi": taxi, "estado": estado},
            )

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {Usuario.objects.count()} usuarios, {Zona.objects.count()} zonas, "
            f"{Linea.objects.count()} líneas, {TaxisFast.objects.count()} taxis, "
            f"{Viaje.objects.count()} viajes."
        ))
