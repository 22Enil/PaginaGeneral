from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import PerfilUsuario, Productos, Categoria, Promocion
from .forms import ProfileForm, ProductoFilterForm, ContactoForm

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
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if not form.is_valid():
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
    template_name = "pcwl/natha_contacto.html"

    def get(self, request, *args, **kwargs):
        # Crear formulario vacío
        form = ContactoForm()
        context_html = {
            'form': form
        }
        return render(request, self.template_name, context_html)

    def post(self, request, *args, **kwargs):
        # Recibir datos del formulario
        form = ContactoForm(request.POST)
        
        if form.is_valid():
            # Se observa en consola
            print("Nuevo mensaje de contacto recibido:")
            print(f"De: {form.cleaned_data['nombre']} ({form.cleaned_data['correo']})")
            print(f"Asunto: {form.cleaned_data['asunto']}")
            
            # Limpiar formulario
            form = ContactoForm()
            
            context_html = {
                'form': form,
                'mensaje_exito': '¡Gracias! Tu mensaje ha sido enviado correctamente.'
            }
            return render(request, self.template_name, context_html)
        
        # Si el formulario no es válido, se devuelve con los errores
        context_html = {
            'form': form
        }
        return render(request, self.template_name, context_html)

# ============================================
# VISTAS DEL CATÁLOGO
# ============================================

class CatalogoView(View):
    """Vista principal del catálogo de productos"""
    template_name = "pcwl/catalogo.html"

    def get(self, request, *args, **kwargs):
        # Obtener todos los productos activos
        productos = Productos.objects.filter(activo=True).select_related('categoria', 'promocion')
        
        # Formulario de filtros
        form = ProductoFilterForm(request.GET)
        
        # Aplicar filtros
        if form.is_valid():
            # Búsqueda por nombre o descripción
            busqueda = form.cleaned_data.get('busqueda')
            if busqueda:
                productos = productos.filter(
                    Q(nombre__icontains=busqueda) | 
                    Q(descripcion__icontains=busqueda)
                )
            
            # Filtro por categoría
            categoria = form.cleaned_data.get('categoria')
            if categoria:
                productos = productos.filter(categoria=categoria)
            
            # Filtro por stock
            en_stock = form.cleaned_data.get('en_stock')
            if en_stock:
                productos = productos.filter(stock__gt=0)
            
            # Filtro por destacados
            destacados = form.cleaned_data.get('destacados')
            if destacados:
                productos = productos.filter(destacado=True)
            
            # Filtro por rango de precios
            precio_min = form.cleaned_data.get('precio_min')
            if precio_min:
                productos = productos.filter(precio__gte=precio_min)
            
            precio_max = form.cleaned_data.get('precio_max')
            if precio_max:
                productos = productos.filter(precio__lte=precio_max)
            
            # Ordenamiento
            orden = form.cleaned_data.get('orden')
            if orden:
                productos = productos.order_by(orden)
        
        # Paginación (12 productos por página)
        paginator = Paginator(productos, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Obtener categorías para el sidebar
        categorias = Categoria.objects.filter(activa=True).prefetch_related('productos')
        
        # Productos destacados para mostrar en el banner
        productos_destacados = Productos.objects.filter(
            activo=True, 
            destacado=True
        )[:4]
        
        context = {
            'productos': page_obj,
            'form': form,
            'categorias': categorias,
            'productos_destacados': productos_destacados,
            'total_productos': productos.count(),
        }
        
        return render(request, self.template_name, context)


class ProductoDetalleView(View):
    """Vista para ver el detalle de un producto"""
    template_name = "pcwl/producto-detalle.html"

    def get(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Productos, pk=pk, activo=True)
        
        # Productos relacionados (misma categoría)
        productos_relacionados = Productos.objects.filter(
            categoria=producto.categoria,
            activo=True
        ).exclude(pk=producto.pk)[:4]
        
        context = {
            'producto': producto,
            'productos_relacionados': productos_relacionados,
        }
        
        return render(request, self.template_name, context)


class ProductosPorCategoriaView(View):
    """Vista para mostrar productos de una categoría específica"""
    template_name = "pcwl/catalogo.html"

    def get(self, request, categoria_id, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=categoria_id, activa=True)
        
        productos = Productos.objects.filter(
            activo=True,
            categoria=categoria
        ).select_related('categoria', 'promocion')
        
        # Paginación
        paginator = Paginator(productos, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Categorías para el sidebar
        categorias = Categoria.objects.filter(activa=True).prefetch_related('productos')
        
        context = {
            'productos': page_obj,
            'categorias': categorias,
            'categoria_actual': categoria,
            'total_productos': productos.count(),
        }
        
        return render(request, self.template_name, context)


# ============================================
# API REST VIEWS (Artículos)
# ============================================

from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Articulo
from .serializers import (
    ArticuloSerializer,
    ArticuloSerializerPretty,
    ArticuloSerializerAll
)

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


class ArticuloViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializers_map = {
        'basic': ArticuloSerializer,
        'pretty': ArticuloSerializerPretty,
        'all': ArticuloSerializerAll,
    }

    def get_serializer_class(self):
        modo = self.kwargs.get('modo', 'basic')
        return self.serializers_map.get(modo, ArticuloSerializer)

    def get_queryset(self):
        return Articulo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ============================================
# API REST VIEWS (Catálogo)
# ============================================

from .serializers import ProductoSerializer, ProductoListSerializer, CategoriaSerializer

class ProductoListAPIView(generics.ListAPIView):
    """API para listar productos"""
    serializer_class = ProductoListSerializer
    
    def get_queryset(self):
        queryset = Productos.objects.filter(activo=True).select_related('categoria', 'promocion')
        
        # Filtros opcionales
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        destacados = self.request.query_params.get('destacados', None)
        if destacados:
            queryset = queryset.filter(destacado=True)
        
        return queryset


class ProductoDetailAPIView(generics.RetrieveAPIView):
    """API para detalle de un producto"""
    queryset = Productos.objects.filter(activo=True)
    serializer_class = ProductoSerializer


class CategoriaListAPIView(generics.ListAPIView):
    """API para listar categorías"""
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer


###########
#Para Test
###########
def sumar(a, b):
    return a + b