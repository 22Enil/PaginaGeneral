from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

# Importas tus modelos y formularios juntos
from .models import PerfilUsuario, Productos, Articulo 
from .forms import ProfileForm

@method_decorator(login_required(login_url='login'), name='dispatch')
class PerfilView(View):
    template_name = "pcwl/perfil-usuario.html"

    def get(self, request, *args, **kwargs):
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
        form = ProfileForm(instance=perfil, user=request.user)
        return render(request, self.template_name, {"perfil": perfil, 'form': form})

    def post(self, request, *args, **kwargs):
        # actualizar campos permitidos: nombre -> user.first_name, biografia -> perfil.biografia
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if not form.is_valid():
            # show errors and re-render
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, f"{field}: {e}")
            return render(request, self.template_name, {"perfil": perfil, 'form': form})

        form.save(user=request.user)
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('perfil')

#Página incial
class Dashboard(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        # 1. Traer productos
        # Usamos .all() para que traiga todo (con o sin foto) y descartar problemas de filtro
        productos = Productos.objects.filter(imagen__isnull=False).exclude(imagen='').order_by('-id')[:5]        
        nombre = "Enil"
        context_html = {
            "nombre_usuario": nombre,
            "productos": productos  # <--- Esta línea es la que llena el carrusel
        }
        return render(request, self.template_name, context_html)

#Página principal
@method_decorator(login_required(login_url='login'), name='dispatch')
class IndexView(View):
    template_name = "pcwl/index.html"

    def get(self, request, *args, **kwargs):
        # 1. Traer productos
        productos = Productos.objects.filter(imagen__isnull=False).exclude(imagen='').order_by('-id')[:5]
        context_html = {
            "productos": productos
        }
        return render(request, self.template_name, context_html)
# Login - Iniciar session
class LoginView(View):
    template_name = "pcwl/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success", "message": "Login correcto"})
        else:
            return JsonResponse({"status": "error", "message": "Usuario o contraseña incorrectos"})
        
# Registro de usuarios
class RegisterView(View):
    template_name = "pcwl/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, self.template_name)

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Usuario registrado con éxito. Ahora puedes iniciar sesión.")
        return redirect("login")

#Logout - Finalizar session
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
    

class ContactView(View):
    template_name = "pcwl/contact.html"

    def get(self, request, *args, **kwargs):
        context_html = {}
        return render(request, self.template_name, context_html)
    

from rest_framework import generics, permissions
from .models import Articulo
from .serializers import ArticuloSerializer

class ArticuloListCreate(generics.ListCreateAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArticuloDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    permission_classes = [permissions.IsAuthenticated]

###############
#Serializers
###############
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Articulo
from .serializers import (
    ArticuloSerializer,
    ArticuloSerializerPretty,
    ArticuloSerializerAll
)

class ArticuloViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # Mapear serializers según "modo"
    serializers_map = {
        'basic': ArticuloSerializer,
        'pretty': ArticuloSerializerPretty,
        'all': ArticuloSerializerAll,
    }

    def get_serializer_class(self):
        modo = self.kwargs.get('modo', 'basic')  # 'basic' por default
        return self.serializers_map.get(modo, ArticuloSerializer)

    def get_queryset(self):
        return Articulo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

###########
#Para Test
###########
def sumar(a, b):
    return a + b
