from django.urls import path #1
#1,#2
from .views import Dashboard, IndexView, LoginView, RegisterView, LogoutView, ContactView, ArticuloListCreate, ArticuloDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView


urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("index/", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("contact/", ContactView.as_view(), name="contact"),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('articulos/', ArticuloListCreate.as_view(), name='articulos'),
    # path('articulos/<int:pk>/', ArticuloDetail.as_view(), name='articulo-detail'),
]


