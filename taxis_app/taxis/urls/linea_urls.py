from django.urls import path
from taxis.views.linea_views import (
    linea_list, linea_detail, linea_create, linea_update, linea_delete,
)

urlpatterns = [
    path('lineas/', linea_list, name='linea_list'),
    path('lineas/nueva/', linea_create, name='linea_create'),
    path('lineas/<int:pk>/', linea_detail, name='linea_detail'),
    path('lineas/<int:pk>/editar/', linea_update, name='linea_update'),
    path('lineas/<int:pk>/eliminar/', linea_delete, name='linea_delete'),
]
