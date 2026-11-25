from decimal import Decimal
from io import StringIO

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from taxis.models import Linea, TaxisFast, Usuario, Viaje, Zona

CLAVE = "clave-segura-123"


def pasajero(username="ana"):
    return Usuario.objects.create_user(username, password=CLAVE, rol="PASAJERO", email=f"{username}@x.com",
                                       first_name=username.title(), last_name="Pérez", telefono="099")


def chofer(username="carlos", estado="EN_BASE", linea=None):
    u = Usuario.objects.create_user(username, password=CLAVE, rol="CHOFER", email=f"{username}@x.com",
                                    first_name=username.title(), last_name="Gómez", telefono="098")
    TaxisFast.objects.create(chofer=u, taxi=f"Taxi {username}", taxi_placa=f"PL-{username}", estado=estado, linea=linea)
    return u


def admin(username="jefe"):
    return Usuario.objects.create_superuser(username, "jefe@x.com", CLAVE)


def viaje(creado_por, **extra):
    return Viaje.objects.create(creado_por=creado_por, origen="Centro", destino="Aeropuerto", **extra)


class ModelosTests(TestCase):
    def test_str_y_get_absolute_url(self):
        zona = Zona.objects.create(nombre="Centro")
        linea = Linea.objects.create(nombre="L1")
        taxi = chofer("carlos").vehiculo
        v = viaje(pasajero("ana"))
        self.assertEqual(str(zona), "Centro")
        self.assertEqual(zona.get_absolute_url(), reverse("zona_detail", args=[zona.pk]))
        self.assertEqual(linea.get_absolute_url(), reverse("linea_detail", args=[linea.pk]))
        self.assertEqual(taxi.get_absolute_url(), reverse("taxi_detail", args=[taxi.pk]))
        self.assertEqual(v.get_absolute_url(), reverse("viaje_detail", args=[v.pk]))

    def test_many_to_many_entre_linea_y_zona(self):
        zona, linea = Zona.objects.create(nombre="Centro"), Linea.objects.create(nombre="L1")
        linea.zonas.add(zona)
        self.assertIn(zona, linea.zonas.all())
        self.assertIn(linea, zona.lineas.all())

    def test_la_tarifa_es_decimal(self):
        taxi = chofer("carlos").vehiculo
        taxi.taxi_tarifa = Decimal("1.25")
        taxi.save()
        taxi.refresh_from_db()
        self.assertEqual(taxi.taxi_tarifa, Decimal("1.25"))

    def test_solo_puede_haber_un_administrador(self):
        admin("jefe")
        with self.assertRaises(Exception):
            admin("otro")


class GruposTests(TestCase):
    def test_existen_los_tres_grupos_con_permisos_distintos(self):
        def permisos(nombre):
            return set(Group.objects.get(name=nombre).permissions.values_list("codename", flat=True))

        self.assertIn("add_viaje", permisos("pasajeros"))
        self.assertNotIn("add_viaje", permisos("choferes"))
        self.assertIn("aceptar_viaje", permisos("choferes"))
        self.assertIn("add_linea", permisos("administradores"))
        self.assertNotIn("add_linea", permisos("pasajeros") | permisos("choferes"))

    def test_cada_usuario_queda_en_el_grupo_de_su_rol(self):
        self.assertEqual(list(pasajero().groups.values_list("name", flat=True)), ["pasajeros"])
        self.assertEqual(list(chofer().groups.values_list("name", flat=True)), ["choferes"])
        self.assertEqual(list(admin().groups.values_list("name", flat=True)), ["administradores"])


class AutenticacionTests(TestCase):
    datos = {"username": "lucia", "first_name": "Lucía", "last_name": "Mora", "telefono": "099",
             "email": "lucia@x.com", "password1": CLAVE, "password2": CLAVE}

    def test_registro_de_pasajero_con_correo_inicia_sesion(self):
        response = self.client.post(reverse("registro_pasajero"), self.datos, follow=True)
        self.assertRedirects(response, reverse("viaje_list"))
        self.assertEqual(Usuario.objects.get(username="lucia").rol, "PASAJERO")

    def test_el_correo_es_obligatorio(self):
        self.client.post(reverse("registro_pasajero"), {**self.datos, "email": ""})
        self.assertFalse(Usuario.objects.filter(username="lucia").exists())

    def test_no_se_puede_colar_un_rol_por_el_formulario(self):
        self.client.post(reverse("registro_pasajero"), {**self.datos, "rol": "ADMIN", "is_superuser": "on"})
        usuario = Usuario.objects.get(username="lucia")
        self.assertEqual(usuario.rol, "PASAJERO")
        self.assertFalse(usuario.is_superuser)

    def test_registro_de_chofer_crea_su_taxi(self):
        self.client.post(reverse("registro_chofer"), {**self.datos, "taxi": "Veloz", "taxi_placa": "abc-123",
                                                      "taxi_tarifa": "1.50"})
        taxi = Usuario.objects.get(username="lucia").vehiculo
        self.assertEqual((taxi.taxi_placa, taxi.taxi_tarifa), ("ABC-123", Decimal("1.50")))

    def test_login_correcto_e_incorrecto(self):
        pasajero("ana")
        malo = self.client.post(reverse("ingresar"), {"username": "ana", "password": "mala"})
        self.assertContains(malo, "Usuario o contraseña incorrectos.")
        bueno = self.client.post(reverse("ingresar"), {"username": "ana", "password": CLAVE})
        self.assertEqual(bueno.status_code, 302)

    def test_logout_solo_por_post(self):
        pasajero("ana")
        self.client.login(username="ana", password=CLAVE)
        self.assertEqual(self.client.get(reverse("salir")).status_code, 405)
        self.client.post(reverse("salir"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_un_anonimo_termina_en_el_login(self):
        url = reverse("linea_create")
        self.assertRedirects(self.client.get(url), f"{reverse('ingresar')}?next={url}")


class PermisosTests(TestCase):
    def setUp(self):
        self.ana, self.carlos, self.jefe = pasajero("ana"), chofer("carlos"), admin("jefe")

    def estado(self, username, url):
        self.client.login(username=username, password=CLAVE)
        codigo = self.client.get(url).status_code
        self.client.logout()
        return codigo

    def test_cada_rol_solo_entra_a_lo_suyo(self):
        self.assertEqual(self.estado("ana", reverse("panel_admin")), 403)
        self.assertEqual(self.estado("ana", reverse("chofer_panel")), 403)
        self.assertEqual(self.estado("ana", reverse("linea_create")), 403)
        self.assertEqual(self.estado("carlos", reverse("viaje_create")), 403)
        self.assertEqual(self.estado("carlos", reverse("panel_admin")), 403)
        self.assertEqual(self.estado("jefe", reverse("panel_admin")), 200)
        self.assertEqual(self.estado("jefe", reverse("linea_create")), 200)

    def test_los_botones_se_ocultan_segun_los_permisos(self):
        self.client.login(username="ana", password=CLAVE)
        self.assertNotContains(self.client.get(reverse("linea_list")), "Nueva línea")
        self.client.login(username="jefe", password=CLAVE)
        self.assertContains(self.client.get(reverse("linea_list")), "Nueva línea")


class CrudLineaTests(TestCase):
    def setUp(self):
        admin("jefe")
        self.client.login(username="jefe", password=CLAVE)
        self.zona = Zona.objects.create(nombre="Centro")

    def test_crear_con_zonas_y_mensaje_de_exito(self):
        response = self.client.post(reverse("linea_create"), {"nombre": "Valle", "zonas": [self.zona.pk]}, follow=True)
        self.assertContains(response, "Línea creada exitosamente.")
        self.assertEqual(list(Linea.objects.get().zonas.all()), [self.zona])

    def test_editar_y_ver_detalle_con_relaciones(self):
        linea = Linea.objects.create(nombre="Sur")
        self.client.post(reverse("linea_update", args=[linea.pk]), {"nombre": "Sur 2", "zonas": [self.zona.pk]})
        linea.refresh_from_db()
        self.assertEqual(linea.nombre, "Sur 2")
        self.assertContains(self.client.get(linea.get_absolute_url()), self.zona.get_absolute_url())

    def test_eliminar_pide_confirmacion_y_solo_borra_con_post(self):
        linea = Linea.objects.create(nombre="Sur")
        url = reverse("linea_delete", args=[linea.pk])
        self.client.get(url)
        self.assertTrue(Linea.objects.exists())
        response = self.client.post(url, follow=True)
        self.assertContains(response, "Línea eliminada exitosamente.")
        self.assertFalse(Linea.objects.exists())

    def test_un_id_inexistente_da_404(self):
        self.assertEqual(self.client.get(reverse("linea_detail", args=[9999])).status_code, 404)

    def test_crud_de_zona(self):
        self.client.post(reverse("zona_create"), {"nombre": "Norte"})
        zona = Zona.objects.get(nombre="Norte")
        self.assertEqual(self.client.get(zona.get_absolute_url()).status_code, 200)
        self.client.post(reverse("zona_delete", args=[zona.pk]))
        self.assertFalse(Zona.objects.filter(nombre="Norte").exists())


class ViajesTests(TestCase):
    def setUp(self):
        self.ana, self.luis = pasajero("ana"), pasajero("luis")
        self.carlos, self.maria = chofer("carlos"), chofer("maria")
        self.v = viaje(self.ana)

    def entrar(self, username):
        self.client.login(username=username, password=CLAVE)

    def test_el_pasajero_crea_y_ve_solo_sus_carreras(self):
        self.entrar("luis")
        self.client.post(reverse("viaje_create"), {"origen": "A", "destino": "B"})
        self.assertEqual(Viaje.objects.filter(creado_por=self.luis).count(), 1)
        self.assertNotContains(self.client.get(reverse("viaje_list")), "Aeropuerto")

    def test_regla_de_propiedad_solo_la_duena_edita_y_elimina(self):
        self.entrar("luis")
        self.assertEqual(self.client.get(reverse("viaje_update", args=[self.v.pk])).status_code, 403)
        self.assertEqual(self.client.post(reverse("viaje_delete", args=[self.v.pk])).status_code, 403)
        self.client.login(username="ana", password=CLAVE)
        response = self.client.post(reverse("viaje_update", args=[self.v.pk]), {"origen": "Nuevo", "destino": "Otro"},
                                    follow=True)
        self.assertContains(response, "Carrera actualizada exitosamente.")
        self.client.post(reverse("viaje_delete", args=[self.v.pk]))
        self.assertFalse(Viaje.objects.filter(pk=self.v.pk).exists())

    def test_el_chofer_acepta_y_completa_su_carrera(self):
        self.entrar("carlos")
        self.client.post(reverse("viaje_aceptar", args=[self.v.pk]))
        self.v.refresh_from_db()
        self.assertEqual((self.v.estado, self.v.taxi), ("ASIGNADO", self.carlos.vehiculo))
        self.assertEqual(TaxisFast.objects.get(chofer=self.carlos).estado, "EN_SERVICIO")
        self.client.post(reverse("viaje_completar", args=[self.v.pk]))
        self.v.refresh_from_db()
        self.assertEqual(self.v.estado, "COMPLETADO")
        self.assertEqual(TaxisFast.objects.get(chofer=self.carlos).estado, "EN_BASE")

    def test_otro_chofer_no_puede_tomar_una_carrera_ya_aceptada(self):
        self.entrar("carlos")
        self.client.post(reverse("viaje_aceptar", args=[self.v.pk]))
        self.client.login(username="maria", password=CLAVE)
        self.client.post(reverse("viaje_aceptar", args=[self.v.pk]))
        self.v.refresh_from_db()
        self.assertEqual(self.v.taxi, self.carlos.vehiculo)
        self.assertEqual(self.client.post(reverse("viaje_completar", args=[self.v.pk])).status_code, 404)

    def test_el_chofer_cambia_su_linea(self):
        linea = Linea.objects.create(nombre="Norte")
        self.entrar("carlos")
        self.client.post(reverse("chofer_taxi_edit"), {"linea": linea.pk, "taxi": "Taxi nuevo", "taxi_placa": "zz-1"})
        taxi = self.carlos.vehiculo
        taxi.refresh_from_db()
        self.assertEqual((taxi.linea, taxi.taxi_placa), (linea, "ZZ-1"))


class DatosDePruebaTests(TestCase):
    def test_cargar_datos_deja_5_o_mas_por_tabla_y_se_puede_repetir(self):
        call_command("cargar_datos", stdout=StringIO())
        for modelo in (Zona, Linea, TaxisFast, Viaje):
            self.assertGreaterEqual(modelo.objects.count(), 5, modelo.__name__)
        total = Usuario.objects.count()
        call_command("cargar_datos", stdout=StringIO())
        self.assertEqual(Usuario.objects.count(), total)
        for username, clave in (("admin", "Admin2026*"), ("chofer1", "Taxis2026*"), ("pasajero1", "Taxis2026*")):
            self.assertTrue(self.client.login(username=username, password=clave), username)
