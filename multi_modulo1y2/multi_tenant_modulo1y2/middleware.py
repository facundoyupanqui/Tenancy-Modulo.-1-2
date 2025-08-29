from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from django.db import connection

class TenantMiddleware(MiddlewareMixin):
    """
    Middleware para manejar el multitenancy.
    Asegura que los usuarios solo puedan acceder a los recursos de su tenant.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.async_mode = False
        # URLs que no requieren autenticación
        self.PUBLIC_URLS = [
            '/admin/',
            '/auth/login/',
            '/auth/register/',
            '/auth/error-no-tenant/',
            '/static/',
            '/media/',
            '/',  # Página principal
        ]
    
    def is_public_url(self, request_path):
        """Verifica si la URL es pública"""
        return any(request_path.startswith(url) for url in self.PUBLIC_URLS)
    
    def process_request(self, request):
        # Ignorar las rutas públicas
        if self.is_public_url(request.path):
            return None
            
        # Si el usuario no está autenticado, redirigir al login
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
            
        # Si el usuario está autenticado, verificar que tenga un tenant asignado
        if not hasattr(request.user, 'tenant') or request.user.tenant is None:
            # Si el usuario no tiene tenant, redirigir a una página de error
            return redirect('/auth/error-no-tenant/')
                
        # Agregar el tenant al request para que esté disponible en las vistas
        request.tenant = request.user.tenant
        return None
        
    def process_response(self, request, response):
        # Agregar información del tenant a la respuesta si está disponible
        if hasattr(request, 'tenant'):
            response['X-Tenant'] = request.tenant.name
        return response

class TenantFilterMiddleware(MiddlewareMixin):
    """
    Middleware para filtrar automáticamente las consultas por tenant.
    """
    def process_request(self, request):
        # Solo aplicar el filtro si el usuario está autenticado y tiene un tenant asignado
        if request.user.is_authenticated and hasattr(request, 'tenant'):
            # Configurar el tenant actual en el thread local para que esté disponible en los managers
            connection.tenant = request.tenant
        return None