"""
URL configuration for config project.

Igual que biblioteca-app: cada módulo de urls de la app se incluye por separado.
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='inicio', permanent=False)),
    path('taxis/', include('taxis.urls.general_urls')),
    path('taxis/', include('taxis.urls.auth_urls')),
    path('taxis/', include('taxis.urls.viaje_urls')),
    path('taxis/', include('taxis.urls.chofer_urls')),
    path('taxis/', include('taxis.urls.panel_urls')),
    path('taxis/', include('taxis.urls.linea_urls')),
]
