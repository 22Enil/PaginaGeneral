from django.contrib import admin

# Register your models here.
from .models import Productos, Promocion, Articulo

#Prueba
@admin.register(Productos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion')  # columnas visibles
    search_fields = ('nombre',)                                     # barra de búsqueda
    list_filter = ('fecha_creacion',)                               # filtros laterales
    ordering = ('nombre',)                                          # orden por defecto

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'descuento', 'fecha_inicio', 'fecha_fin')  # columnas visibles
    list_filter = ('fecha_inicio', 'fecha_fin')                            # filtros por fecha


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'owner', 'creado')   # columnas visibles
    list_filter = ('creado', 'owner')              # filtros
    search_fields = ('titulo', 'contenido')        # buscador
    ordering = ('-creado',)

