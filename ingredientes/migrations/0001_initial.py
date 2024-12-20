# Generated by Django 5.1.1 on 2024-12-07 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Receta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255)),
                ("descripcion", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Ingrediente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255)),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "precio_por_kg",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("link_imagen", models.URLField(blank=True, max_length=500, null=True)),
                ("fecha_agregado", models.DateTimeField(auto_now_add=True)),
                (
                    "supermercado",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "receta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredientes",
                        to="ingredientes.receta",
                    ),
                ),
            ],
        ),
    ]
