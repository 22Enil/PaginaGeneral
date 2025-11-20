from rest_framework import serializers
from .models import Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ['id','titulo','contenido','owner','creado']
        read_only_fields = ['owner','creado']
