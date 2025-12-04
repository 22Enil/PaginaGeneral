from rest_framework import serializers
from .models import Articulo, Productos, Categoria, Promocion


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ['id','titulo','contenido','owner','creado']
        read_only_fields = ['owner','creado']


class ArticuloSerializerPretty(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Articulo
        fields = ['id', 'titulo', 'contenido', 'owner', 'creado']
        read_only_fields = ['owner', 'creado']


class ArticuloSerializerAll(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Articulo
        fields = '__all__'
        read_only_fields = ['owner', 'creado']


# ============================================
# SERIALIZERS PARA EL CATÁLOGO
# ============================================

class CategoriaSerializer(serializers.ModelSerializer):
    total_productos = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activa', 'total_productos']
    
    def get_total_productos(self, obj):
        return obj.productos.filter(activo=True).count()


class PromocionSerializer(serializers.ModelSerializer):
    esta_activa = serializers.ReadOnlyField()
    
    class Meta:
        model = Promocion
        fields = ['id', 'descuento', 'fecha_inicio', 'fecha_fin', 'esta_activa']


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    promocion = PromocionSerializer(read_only=True)
    precio_con_promocion = serializers.ReadOnlyField()
    tiene_stock = serializers.ReadOnlyField()
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Productos
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'stock', 
            'imagen', 'imagen_url', 'categoria', 'categoria_nombre',
            'activo', 'destacado', 'fecha_creacion', 'fecha_actualizacion',
            'promocion', 'precio_con_promocion', 'tiene_stock'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None


class ProductoListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    precio_con_promocion = serializers.ReadOnlyField()
    tiene_promocion = serializers.SerializerMethodField()
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Productos
        fields = [
            'id', 'nombre', 'precio', 'stock', 'imagen_url',
            'categoria_nombre', 'destacado', 'precio_con_promocion',
            'tiene_promocion'
        ]
    
    def get_tiene_promocion(self, obj):
        return hasattr(obj, 'promocion') and obj.promocion.esta_activa
    
    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None