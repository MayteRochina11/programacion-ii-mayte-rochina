from django.urls import path
from taxis.views.panel_views import (
    panel_admin, panel_choferes, panel_pasajeros, panel_viajes,
)

urlpatterns = [
    path('panel/', panel_admin, name='panel_admin'),
    path('panel/choferes/', panel_choferes, name='panel_choferes'),
    path('panel/pasajeros/', panel_pasajeros, name='panel_pasajeros'),
    path('panel/viajes/', panel_viajes, name='panel_viajes'),
]
