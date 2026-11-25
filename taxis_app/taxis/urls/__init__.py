from taxis.urls.general_urls import urlpatterns as general_urls
from taxis.urls.auth_urls import urlpatterns as auth_urls
from taxis.urls.viaje_urls import urlpatterns as viaje_urls
from taxis.urls.chofer_urls import urlpatterns as chofer_urls
from taxis.urls.panel_urls import urlpatterns as panel_urls
from taxis.urls.linea_urls import urlpatterns as linea_urls
from taxis.urls.zona_urls import urlpatterns as zona_urls
from taxis.urls.taxi_urls import urlpatterns as taxi_urls

urlpatterns = (
    general_urls + auth_urls + viaje_urls + chofer_urls
    + panel_urls + linea_urls + zona_urls + taxi_urls
)
