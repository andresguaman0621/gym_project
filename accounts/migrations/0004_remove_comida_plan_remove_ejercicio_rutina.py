# Generated by Django 5.1.1 on 2024-12-08 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_superadministrador_comida_cantidad_comida_nombre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comida',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='rutina',
        ),
    ]