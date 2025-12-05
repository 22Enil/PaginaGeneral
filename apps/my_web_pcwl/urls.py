from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views import (
    Dashboard, 
    IndexView, 
    LoginView, 
    RegisterView, 
    LogoutView, 
    ContactView, 
    PerfilView,
    ArticuloListCreate, 
    ArticuloDetail,
    # Vistas del Catálogo
    CatalogoView,
    ProductoDetalleView,
    ProductosPorCategoriaView,
    # API del Catálogo
    ProductoListAPIView,
    ProductoDetailAPIView,
    CategoriaListAPIView,
)


urlpatterns = [
    # Rutas principales
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("index/", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("perfil/", PerfilView.as_view(), name="perfil"),
    
    # Rutas del Catálogo
    path("catalogo/", CatalogoView.as_view(), name="catalogo"),
    path("producto/<int:pk>/", ProductoDetalleView.as_view(), name="producto_detalle"),
    path("categoria/<int:categoria_id>/", ProductosPorCategoriaView.as_view(), name="productos_categoria"),
    
    # API REST - Catálogo
    path("api/productos/", ProductoListAPIView.as_view(), name="api_productos"),
    path("api/producto/<int:pk>/", ProductoDetailAPIView.as_view(), name="api_producto_detalle"),
    path("api/categorias/", CategoriaListAPIView.as_view(), name="api_categorias"),

    # API REST - Artículos (comentadas)
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('articulos/', ArticuloListCreate.as_view(), name='articulos'),
    # path('articulos/<int:pk>/', ArticuloDetail.as_view(), name='articulo-detail'),
]