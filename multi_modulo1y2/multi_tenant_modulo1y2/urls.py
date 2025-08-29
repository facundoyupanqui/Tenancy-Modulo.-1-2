from django.contrib import admin
from django.urls import path, include
from auth_views.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('auth_views.urls')),
    path('productos/', include('productos.urls')),
    path('clientes/', include('clientes.urls')),
    path('users/', include('users.urls')),
    path('citas/', include('citas_medicas.urls')),
]