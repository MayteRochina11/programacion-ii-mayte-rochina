# taxis/tests.py
from django.test import TestCase
from django.urls import reverse

from .models import Linea, TaxisFast


class LineaModelTests(TestCase):
    def test_str_devuelve_el_nombre(self):
        linea = Linea.objects.create(nombre="Centro", zona="Centro histórico")
        self.assertEqual(str(linea), "Centro")

    def test_borrar_linea_no_borra_sus_taxis(self):
        linea = Linea.objects.create(nombre="Norte")
        taxi = TaxisFast.objects.create(taxi="Azul", linea=linea)
        linea.delete()
        taxi.refresh_from_db()
        self.assertIsNone(taxi.linea)


class TaxisFastModelTests(TestCase):
    def test_estado_por_defecto_es_en_base(self):
        taxi = TaxisFast.objects.create(taxi="Amarillo")
        self.assertEqual(taxi.estado, TaxisFast.Estado.EN_BASE)

    def test_relacion_uno_a_muchos(self):
        linea = Linea.objects.create(nombre="Centro")
        TaxisFast.objects.create(taxi="Amarillo", linea=linea)
        TaxisFast.objects.create(taxi="Azul", linea=linea)
        self.assertEqual(linea.taxis.count(), 2)


class HomeViewTests(TestCase):
    def test_home_responde_200_y_muestra_taxis(self):
        TaxisFast.objects.create(taxi="Rosa", taxi_placa="PPP 2223")
        response = self.client.get(reverse("taxis:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxis/home.html")
        self.assertContains(response, "Rosa")
        self.assertContains(response, "PPP 2223")

    def test_home_cuenta_taxis_por_estado(self):
        TaxisFast.objects.create(taxi="A", estado=TaxisFast.Estado.EN_SERVICIO)
        TaxisFast.objects.create(taxi="B", estado=TaxisFast.Estado.EN_SERVICIO)
        TaxisFast.objects.create(taxi="C", estado=TaxisFast.Estado.EN_BASE)
        response = self.client.get(reverse("taxis:home"))
        self.assertEqual(response.context["total_en_servicio"], 2)
        self.assertEqual(response.context["total_en_base"], 1)


class TaxiCreateViewTests(TestCase):
    def test_get_muestra_formulario(self):
        response = self.client.get(reverse("taxis:taxi_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_post_valido_crea_taxi_y_redirige(self):
        linea = Linea.objects.create(nombre="Norte")
        response = self.client.post(reverse("taxis:taxi_create"), {
            "linea": linea.pk,
            "taxi": "Verde",
            "taxi_placa": "ABC 1234",
            "taxi_chofer": "Ana",
            "taxi_tarifa": "1.25",
            "estado": TaxisFast.Estado.EN_SERVICIO,
        })
        self.assertRedirects(response, reverse("taxis:home"))
        taxi = TaxisFast.objects.get(taxi="Verde")
        self.assertEqual(taxi.linea, linea)
        self.assertEqual(taxi.estado, TaxisFast.Estado.EN_SERVICIO)

    def test_post_invalido_no_crea_nada(self):
        response = self.client.post(reverse("taxis:taxi_create"), {"taxi": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TaxisFast.objects.exists())


class LineaViewTests(TestCase):
    def test_lista_de_lineas(self):
        Linea.objects.create(nombre="Sur", zona="Sur")
        response = self.client.get(reverse("taxis:lineas_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sur")

    def test_crear_linea_y_redirige_a_la_lista(self):
        response = self.client.post(reverse("taxis:linea_create"), {
            "nombre": "Valle",
            "zona": "Los Chillos",
            "descripcion": "",
        })
        self.assertRedirects(response, reverse("taxis:lineas_lista"))
        self.assertTrue(Linea.objects.filter(nombre="Valle").exists())


class SobreNosotrosViewTests(TestCase):
    def test_responde_200(self):
        response = self.client.get(reverse("taxis:sobre_nosotros"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sobre TaxisFast")
