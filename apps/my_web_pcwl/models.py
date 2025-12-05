import os
import uuid
from django.db import models
from django.conf import settings

# Create your models here.

# Función para definir la ruta de subida de imágenes de productos
def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('productos', filename)

# Modelo Categoría → para organizar productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

# Modelo Producto → representa una tabla con los productos
from django.db import models
class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='productos'
    )
    activo = models.BooleanField(default=True)  # Para ocultar productos sin eliminarlos
    destacado = models.BooleanField(default=False)  # Para productos destacados en el catálogo
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):                                    # Método que define cómo se mostrará el objeto como texto
        return self.nombre                                # Al imprimir un producto, se verá su nombre
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre
    
    @property
    def tiene_stock(self):
        """Retorna True si hay stock disponible"""
        return self.stock > 0
    
    @property
    def precio_con_promocion(self):
        """Retorna el precio con descuento si tiene promoción activa"""
        try:
            if hasattr(self, 'promocion'):
                from django.utils import timezone
                hoy = timezone.now().date()
                if self.promocion.fecha_inicio <= hoy <= self.promocion.fecha_fin:
                    descuento = self.precio * (self.promocion.descuento / 100)
                    return self.precio - descuento
        except:
            pass
        return self.precio

# Modelo Promocion → cada promoción pertenece a un producto
class Promocion(models.Model):
    producto = models.OneToOneField(
        Productos,
        on_delete=models.CASCADE,
        related_name='promocion'
    )
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Porcentaje de descuento (ej. 10.00 para 10%)"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"

    def __str__(self):
        return f"Promoción de {self.producto.nombre} ({self.descuento}%)"
    
    @property
    def esta_activa(self):
        """Verifica si la promoción está activa hoy"""
        from django.utils import timezone
        hoy = timezone.now().date()
        return self.fecha_inicio <= hoy <= self.fecha_fin

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-creado']

    def __str__(self):
        return self.titulo

# Función para definir la ruta de subida de imágenes de perfil
def user_profile_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_pics', filename)

# modelo PerfilUsuario para extender el modelo de usuario
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)
    imagen_perfil = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"