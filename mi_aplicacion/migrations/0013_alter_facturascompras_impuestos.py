# Generated by Django 5.1.1 on 2024-10-18 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mi_aplicacion", "0012_merge_20241018_0230"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facturascompras",
            name="impuestos",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
