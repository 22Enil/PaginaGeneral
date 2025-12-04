from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

# Register your models here.
from .models import Productos, Promocion, Articulo, PerfilUsuario, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'contar_productos')
    search_fields = ('nombre',)
    list_filter = ('activa',)
    ordering = ('nombre',)
    
    def contar_productos(self, obj):
        """Cuenta cuántos productos tiene la categoría"""
        count = obj.productos.count()
        return f"{count} producto(s)"
    contar_productos.short_description = 'Cantidad de Productos'


@admin.register(Productos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_mostrar', 'stock_mostrar', 'imagen_preview', 'activo', 'destacado', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activo', 'destacado', 'categoria', 'fecha_creacion')
    ordering = ('-fecha_creacion',)
    list_editable = ('activo', 'destacado')  # Permite editar directamente desde la lista
    readonly_fields = ('imagen_preview_grande', 'fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Precio y Stock', {
            'fields': ('precio', 'stock')
        }),
        ('Imagen', {
            'fields': ('imagen', 'imagen_preview_grande')
        }),
        ('Configuración', {
            'fields': ('activo', 'destacado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)  # Sección colapsable
        }),
    )
    
    def precio_mostrar(self, obj):
        """Muestra el precio con formato"""
        return f"${obj.precio:,.2f}"
    precio_mostrar.short_description = 'Precio'
    precio_mostrar.admin_order_field = 'precio'
    
    def stock_mostrar(self, obj):
        """Muestra el stock con colores según disponibilidad"""
        if obj.stock == 0:
            color = 'red'
            texto = 'Sin stock'
        elif obj.stock < 10:
            color = 'orange'
            texto = f'{obj.stock} unidades'
        else:
            color = 'green'
            texto = f'{obj.stock} unidades'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, texto
        )
    stock_mostrar.short_description = 'Stock'
    stock_mostrar.admin_order_field = 'stock'
    
    def imagen_preview(self, obj):
        """Miniatura de la imagen en la lista"""
        if obj.imagen:
            try:
                url = obj.imagen.url
                return format_html(
                    '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:4px;" />',
                    url
                )
            except:
                return "-"
        return "-"
    imagen_preview.short_description = 'Imagen'
    
    def imagen_preview_grande(self, obj):
        """Preview más grande para el formulario de edición"""
        if obj.imagen:
            try:
                url = obj.imagen.url
                return format_html(
                    '<img src="{}" style="max-width:300px;max-height:300px;object-fit:contain;border:1px solid #ddd;padding:5px;" />',
                    url
                )
            except:
                return "Imagen no disponible"
        return "Sin imagen"
    imagen_preview_grande.short_description = 'Vista Previa'


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'descuento_mostrar', 'fecha_inicio', 'fecha_fin', 'estado_promocion')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('producto__nombre',)
    ordering = ('-fecha_inicio',)
    
    def descuento_mostrar(self, obj):
        """Muestra el descuento con formato"""
        return f"{obj.descuento}%"
    descuento_mostrar.short_description = 'Descuento'
    descuento_mostrar.admin_order_field = 'descuento'
    
    def estado_promocion(self, obj):
        """Muestra si la promoción está activa, próxima o expirada"""
        hoy = timezone.now().date()
        
        if obj.fecha_inicio > hoy:
            return format_html(
                '<span style="color: blue; font-weight: bold;">📅 Próxima</span>'
            )
        elif obj.fecha_fin < hoy:
            return format_html(
                '<span style="color: gray;">⏹️ Expirada</span>'
            )
        else:
            return format_html(
                '<span style="color: green; font-weight: bold;">✅ Activa</span>'
            )
    estado_promocion.short_description = 'Estado'


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'owner', 'creado')
    list_filter = ('creado', 'owner')
    search_fields = ('titulo', 'contenido')
    ordering = ('-creado',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'phone_number', 'imagen_preview', 'biografia_short')
    search_fields = ('usuario__username', 'phone_number')
    raw_id_fields = ('usuario',)
    readonly_fields = ('imagen_preview',)
    list_select_related = ('usuario',)

    def imagen_preview(self, obj):
        if obj.imagen_perfil:
            try:
                url = obj.imagen_perfil.url
            except Exception:
                url = getattr(obj.imagen_perfil, 'name', None)
            if url:
                return format_html(
                    '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />',
                    url
                )
        return "-"
    imagen_preview.short_description = 'Foto'

    def biografia_short(self, obj):
        if obj.biografia:
            text = obj.biografia
            return text if len(text) <= 75 else text[:72] + '...'
        return '-'
    biografia_short.short_description = 'Biografía'