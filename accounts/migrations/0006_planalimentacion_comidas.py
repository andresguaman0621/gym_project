# Generated by Django 5.1.1 on 2024-12-08 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rutinaentrenamiento_ejercicios'),
    ]

    operations = [
        migrations.AddField(
            model_name='planalimentacion',
            name='comidas',
            field=models.ManyToManyField(blank=True, related_name='planes', to='accounts.comida'),
        ),
    ]
