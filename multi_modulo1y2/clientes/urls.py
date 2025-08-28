from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:pk>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/crear/', views.crear_cliente, name='crear_cliente'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
] 