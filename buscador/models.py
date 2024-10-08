from django.db import models

# Create your models here.
class ProductoBase(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del producto
    precio = models.CharField(max_length=50)  # Precio del producto
    precio_por_kg = models.CharField(max_length=50)  # Precio por kg
    link_imagen = models.CharField(max_length=500)
    class Meta: 
        abstract = True

class ProductoTablaAlcampo(ProductoBase):
    class Meta: 
        db_table = 'productos_alcampo'
    def __str__(self):
        return self.nombre
class ProductoTablaCarrefour(ProductoBase):
    class Meta: 
        db_table = 'productos_carrefour'
    def __str__(self):
        return self.nombre
class ProductoTablaEroski(ProductoBase):
    class Meta: 
        db_table = 'productos_eroski'

    def __str__(self):
        return self.nombre