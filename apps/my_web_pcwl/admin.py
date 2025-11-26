from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Productos, Promocion, Articulo, PerfilUsuario


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

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'phone_number', 'imagen_preview', 'biografia_short')  # columnas visibles
    search_fields = ('usuario__username', 'phone_number')  # buscador por nombre de usuario y teléfono
    raw_id_fields = ('usuario',)
    readonly_fields = ('imagen_preview',)
    list_select_related = ('usuario',)

    def imagen_preview(self, obj):
        if obj.imagen_perfil:
            try:
                url = obj.imagen_perfil.url
            except Exception:
                # si no hay URL accesible, mostrar la ruta de archivo
                url = getattr(obj.imagen_perfil, 'name', None)
            if url:
                return format_html('<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />', url)
        return "-"
    imagen_preview.short_description = 'Foto'

    def biografia_short(self, obj):
        if obj.biografia:
            text = obj.biografia
            return text if len(text) <= 75 else text[:72] + '...'
        return '-'
    biografia_short.short_description = 'Biografía'

