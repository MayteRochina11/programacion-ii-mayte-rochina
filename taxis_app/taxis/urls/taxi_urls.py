from django.urls import path
from taxis.views.taxi_views import taxi_list, taxi_detail

urlpatterns = [
    path('flota/', taxi_list, name='taxi_list'),
    path('flota/<int:pk>/', taxi_detail, name='taxi_detail'),
]
