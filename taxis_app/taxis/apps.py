from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _crear_grupos_tras_migrar(sender, using="default", **kwargs):
    from django.db import DatabaseError

    from taxis.grupos import crear_grupos

    try:
        crear_grupos(using=using)
    except DatabaseError:
        pass


class TaxisConfig(AppConfig):
    name = 'taxis'

    def ready(self):
        post_migrate.connect(_crear_grupos_tras_migrar, sender=self)
