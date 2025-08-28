from django.urls import path
from . import views

app_name = 'auth_views'

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 