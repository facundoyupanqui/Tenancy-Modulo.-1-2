from django.urls import path
from . import views

app_name = 'citas_medicas'

urlpatterns = [
    path('', views.cita_list, name='cita_list'),
    path('nueva/', views.cita_create, name='cita_create'),
    path('<int:pk>/', views.cita_detail, name='cita_detail'),
    path('<int:pk>/editar/', views.cita_update, name='cita_update'),
    path('<int:pk>/cancelar/', views.cita_cancel, name='cita_cancel'),
    path('doctores/', views.doctor_list, name='doctor_list'),
    path('doctores/<int:pk>/', views.doctor_detail, name='doctor_detail'),
]
