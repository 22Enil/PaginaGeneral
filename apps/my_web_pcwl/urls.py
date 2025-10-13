from django.urls import path #1
#1,#2
from .views import Dashboard, IndexView, LoginView, RegisterView, LogoutView, ContactView

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("index/", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("contact/", ContactView.as_view(), name="contact"),
]
