from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ArticuloListCreate, ArticuloDetail

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('articulos/', ArticuloListCreate.as_view(), name='articulos'),
    path('articulos/<int:pk>/', ArticuloDetail.as_view(), name='articulo-detail'),
]
