# Generated by Django 5.1 on 2024-09-04 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mi_aplicacion', '0003_remove_proveedor_status_proveedor_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleorden',
            name='precio_unitario',
        ),
        migrations.RemoveField(
            model_name='detalleorden',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='total',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='precio',
        ),
    ]
