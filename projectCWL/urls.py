"""
URL configuration for projectCWL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Nota: En desarrollo (`DEBUG = True`) añadimos `static()` para que Django
# sirva archivos estáticos y de medios directamente. Esto NO debe usarse
# en producción: en producción los archivos estáticos y media deben ser
# servidos por WhiteNoise o por el servidor web (nginx, apache, etc.).

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.my_web_pcwl.urls")),  # incluimos urls de la app
    path("api/", include("apps.my_web_pcwl.urls_api")),  # API separada
]

if settings.DEBUG:
    # Sirve archivos estáticos reunidos en `STATIC_ROOT` cuando DEBUG=True
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Sirve archivos subidos por usuarios (MEDIA) durante desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
