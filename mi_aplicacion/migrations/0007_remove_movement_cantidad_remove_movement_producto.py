# Generated by Django 5.1 on 2024-09-06 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mi_aplicacion', '0006_alter_movement_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movement',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='movement',
            name='producto',
        ),
    ]
