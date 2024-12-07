
from django.db import models


class Receta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    class Meta:
        db_table = 'Recetas'

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    receta = models.ForeignKey(Receta, related_name='ingredientes', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_por_kg = models.CharField(max_length=50, null=True, blank=True)
    link_imagen = models.URLField(max_length=500, null=True, blank=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    supermercado = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Ingredientes'

    def __str__(self):
        return f"{self.nombre} ({self.supermercado}) - {self.precio}"
