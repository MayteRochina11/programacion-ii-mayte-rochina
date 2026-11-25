from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('taxis', '0002_zonas_y_tarifa_decimal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viaje',
            old_name='pasajero',
            new_name='creado_por',
        ),
        migrations.AlterField(
            model_name='viaje',
            name='creado_por',
            field=models.ForeignKey(
                limit_choices_to={'rol': 'PASAJERO'},
                on_delete=django.db.models.deletion.PROTECT,
                related_name='viajes_pedidos',
                to=settings.AUTH_USER_MODEL,
                verbose_name='pasajero',
            ),
        ),
        migrations.AlterModelOptions(
            name='viaje',
            options={
                'ordering': ['-created_at'],
                'permissions': [
                    ('aceptar_viaje', 'Puede aceptar carreras pendientes'),
                    ('completar_viaje', 'Puede completar sus propias carreras'),
                ],
                'verbose_name': 'viaje',
                'verbose_name_plural': 'viajes',
            },
        ),
    ]
