# Generated by Django 5.1.1 on 2024-12-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_comida_plan_remove_ejercicio_rutina'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutinaentrenamiento',
            name='ejercicios',
            field=models.ManyToManyField(blank=True, related_name='rutinas', to='accounts.ejercicio'),
        ),
    ]