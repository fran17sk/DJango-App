# Generated by Django 5.1 on 2024-09-05 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_aplicacion', '0006_ordencompra_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturascompras',
            name='detalles',
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('preciounitario', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_aplicacion.facturascompras')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mi_aplicacion.producto')),
            ],
        ),
    ]
