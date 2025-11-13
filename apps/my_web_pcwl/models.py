from django.db import models # Importa el módulo 'models' de Django para crear las tablas (modelos)
# Create your models here.

# Modelo Producto → representa una tabla con los productos
class Productos(models.Model):
    nombre = models.CharField(max_length=100)             # Campo de texto corto (nombre del producto)
    descripcion = models.TextField(blank=True)            # Texto largo, puede quedar vacío
    precio = models.DecimalField(max_digits=8, decimal_places=2)  # Precio con 2 decimales (ej. 199.99)
    stock = models.PositiveIntegerField(default=0)        # Cantidad disponible (solo números positivos)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)  # Fecha automática al crear el producto

    def __str__(self):                                    # Método que define cómo se mostrará el objeto como texto
        return self.nombre                                # Al imprimir un producto, se verá su nombre

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