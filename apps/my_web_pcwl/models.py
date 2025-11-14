from django.db import models # Importa el módulo 'models' de Django para crear las tablas (modelos)
# Create your models here.

# Modelo Producto → representa una tabla con los productos
from django.db import models
class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre                               # Al imprimir un producto, se verá su nombre

# Modelo Promocion → cada promoción pertenece a un producto
class Promocion(models.Model):
    # Relación uno a uno: cada producto puede tener solo UNA promoción
    producto = models.OneToOneField(
        Productos,                     # Relaciona con el modelo Producto
        on_delete=models.CASCADE,     # Si se borra el producto, se borra también su promoción
        related_name='promocion'      # Permite acceder desde Producto con 'producto.promocion'
    )
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Porcentaje de descuento (ej. 10.00 para 10%)"  # Muestra una ayuda en el panel admin
    )
    fecha_inicio = models.DateField()    # Fecha en la que inicia la promoción
    fecha_fin = models.DateField()       # Fecha en la que termina la promoción

    def __str__(self):                   # Representación legible del objeto Promocion
        # Muestra el nombre del producto y el porcentaje de descuento
        return f"Promoción de {self.producto.nombre} ({self.descuento}%)"