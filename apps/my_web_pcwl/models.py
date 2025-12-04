import os
import uuid
from django.db import models # Importa el módulo 'models' de Django para crear las tablas (modelos)
from django.conf import settings #
# Create your models here.

# Modelo Producto → representa una tabla con los productos
from django.db import models
class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

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
    
#Movimiento de importación al inicio para mejor organización
#from django.conf import settings

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

# Función para definir la ruta de subida de imágenes de perfil
def user_profile_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_pics', filename)

#modelo PerfilUsuario para extender el modelo de usuario
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)
    imagen_perfil = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return f"Perfil de {self.usuario.username}"