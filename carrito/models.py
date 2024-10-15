from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_por_kg = models.DecimalField(max_digits=10, decimal_places=2)
    link_imagen = models.URLField(max_length=200)
    supermercado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class CarritoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
