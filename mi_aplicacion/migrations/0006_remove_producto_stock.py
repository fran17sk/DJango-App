# Generated by Django 5.1 on 2024-08-13 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mi_aplicacion', '0005_rename_productos_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='stock',
        ),
    ]
