from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ArticuloListCreate, ArticuloDetail

from .views import ArticuloViewSet

articulos_list = ArticuloViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

articulos_detail = ArticuloViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('articulos/', ArticuloListCreate.as_view(), name='articulos'),
    path('articulos/<int:pk>/', ArticuloDetail.as_view(), name='articulo-detail'),

    path('articulos/<str:modo>/', articulos_list),
    path('articulos/<str:modo>/<int:pk>/', articulos_detail),
]
