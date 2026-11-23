from django.urls import path
from taxis.views.zona_views import (
    zona_list, zona_detail, zona_create, zona_update, zona_delete,
)

urlpatterns = [
    path('zonas/', zona_list, name='zona_list'),
    path('zonas/nueva/', zona_create, name='zona_create'),
    path('zonas/<int:pk>/', zona_detail, name='zona_detail'),
    path('zonas/<int:pk>/editar/', zona_update, name='zona_update'),
    path('zonas/<int:pk>/eliminar/', zona_delete, name='zona_delete'),
]
