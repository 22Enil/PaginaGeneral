from django.test import TestCase

# Create your tests here.
from .views import sumar

#Prueba basicas
class PruebasBasicas(TestCase):

    def test_sumar(self):
        resultado = sumar(2, 3)
        self.assertEqual(resultado, 5)

# Esto es un cambio de prueba
# Esto es otra prueab
