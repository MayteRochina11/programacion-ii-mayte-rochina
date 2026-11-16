from django.urls import path
from taxis.views.chofer_views import chofer_panel, chofer_disponibilidad, chofer_taxi_edit

urlpatterns = [
    path('chofer/', chofer_panel, name='chofer_panel'),
    path('chofer/taxi/', chofer_taxi_edit, name='chofer_taxi_edit'),
    path('chofer/disponibilidad/', chofer_disponibilidad, name='chofer_disponibilidad'),
]
