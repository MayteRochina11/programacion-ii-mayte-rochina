from django.urls import path
from taxis.views.general_views import inicio, sobre_nosotros

urlpatterns = [
    path('', inicio, name='inicio'),
    path('sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),
]
