from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('<int:pk>/', views.producto_detail, name='producto_detail'),
    path('nuevo/', views.producto_create, name='producto_create'),
    path('<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
]