from decimal import Decimal, InvalidOperation

import django.core.validators
from django.db import migrations, models


def copiar_tarifa_a_decimal(apps, schema_editor):
    TaxisFast = apps.get_model("taxis", "TaxisFast")
    for taxi in TaxisFast.objects.all():
        texto = (taxi.taxi_tarifa or "").strip().replace(",", ".")
        try:
            valor = Decimal(texto).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            valor = None
        if valor is not None and not (0 <= valor < 10000):
            valor = None
        taxi.taxi_tarifa_nueva = valor
        taxi.save(update_fields=["taxi_tarifa_nueva"])


class Migration(migrations.Migration):
    dependencies = [
        ('taxis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'zona',
                'verbose_name_plural': 'zonas',
                'ordering': ['nombre'],
            },
        ),
        migrations.AlterModelOptions(
            name='linea',
            options={'ordering': ['nombre'], 'verbose_name': 'línea', 'verbose_name_plural': 'líneas'},
        ),
        migrations.AlterModelOptions(
            name='taxisfast',
            options={'ordering': ['taxi'], 'verbose_name': 'taxi', 'verbose_name_plural': 'taxis'},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['username'], 'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios'},
        ),
        migrations.AddField(
            model_name='linea',
            name='zonas',
            field=models.ManyToManyField(blank=True, related_name='lineas', to='taxis.zona'),
        ),
        migrations.AddField(
            model_name='taxisfast',
            name='taxi_tarifa_nueva',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.RunPython(copiar_tarifa_a_decimal, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='taxisfast',
            name='taxi_tarifa',
        ),
        migrations.RenameField(
            model_name='taxisfast',
            old_name='taxi_tarifa_nueva',
            new_name='taxi_tarifa',
        ),
        migrations.AlterField(
            model_name='taxisfast',
            name='taxi_tarifa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
