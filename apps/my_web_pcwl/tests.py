from django.test import TestCase

# Create your tests here.
from .views import sumar

class PruebasBasicas(TestCase):

    def test_sumar(self):
        resultado = sumar(2, 3)
        self.assertEqual(resultado, 5)

