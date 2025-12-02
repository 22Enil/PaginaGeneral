from rest_framework import serializers
from .models import Articulo

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
        fields = '__all__'       # incluye todos los campos del modelo
        read_only_fields = ['owner', 'creado']
