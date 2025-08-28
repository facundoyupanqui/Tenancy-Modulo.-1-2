from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import re

class TenantMiddleware:
    """
    Middleware para manejar la autenticación y filtrado por tenant
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Procesar la solicitud antes de que llegue a la vista
        request = self.process_request(request)
        
        # Obtener la respuesta
        response = self.get_response(request)
        
        # Procesar la respuesta antes de enviarla al cliente
        response = self.process_response(request, response)
        
        return response

    def process_request(self, request):
        """Procesar la solicitud antes de que llegue a la vista"""
        
        # URLs que no requieren autenticación
        public_urls = [
            '/admin/login/',
            '/login/',
            '/logout/',
            '/static/',
            '/media/',
        ]
        
        # Verificar si la URL actual es pública
        current_path = request.path_info.lstrip('/')
        is_public = any(re.match(pattern.lstrip('/'), current_path) for pattern in public_urls)
        
        # Si es una URL pública, no hacer nada
        if is_public:
            return request
        
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            # Redirigir al login si no está autenticado
            return redirect('login')
        
        # Verificar si el usuario tiene un tenant asignado
        try:
            tenant = request.user.usuariotenant.tenant
            request.tenant = tenant
        except:
            # Si no tiene tenant, redirigir al login
            messages.error(request, 'No tienes un tenant asignado')
            return redirect('login')
        
        return request

    def process_response(self, request, response):
        """Procesar la respuesta antes de enviarla al cliente"""
        
        # Agregar información del tenant a la respuesta si está disponible
        if hasattr(request, 'tenant'):
            response['X-Tenant'] = request.tenant.slug
        
        return response

class TenantFilterMiddleware:
    """
    Middleware para filtrar consultas por tenant
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Procesar la vista antes de que se ejecute"""
        
        # Solo aplicar filtros si el usuario está autenticado y tiene tenant
        if hasattr(request, 'tenant') and request.tenant:
            # Aquí se pueden agregar filtros adicionales por tenant
            pass
        
        return None 