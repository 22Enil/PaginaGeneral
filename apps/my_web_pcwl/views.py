from django.shortcuts import render, redirect #en automatico
# Create your views here.
#1
from django.views import View
#2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
#3
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#4
from django.http import JsonResponse

#Página incial
class Dashboard(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        nombre = "Enil"
        context_html = {
            "nombre_usuario": nombre
        }
        return render(request, self.template_name, context_html)

#Página principal
@method_decorator(login_required(login_url='login'), name='dispatch')
class IndexView(View):
    template_name = "pcwl/index.html"

    def get(self, request, *args, **kwargs):
        context_html = {}
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
