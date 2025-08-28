from django.contrib import admin
from django.contrib.auth.models import User
from .models import Cliente, UsuarioTenant
from productos.models import Tenant

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'tenant', 'email', 'telefono', 'is_active']
    list_filter = ['tenant', 'is_active', 'created_at']
    search_fields = ['nombre', 'apellido', 'email', 'telefono']
    list_editable = ['is_active']
    ordering = ['tenant', 'apellido', 'nombre']
    
    def get_queryset(self, request):
        """Filtrar clientes por tenant del usuario"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Aquí implementaremos la lógica de filtrado por tenant
        return qs

@admin.register(UsuarioTenant)
class UsuarioTenantAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant', 'rol', 'is_active', 'created_at']
    list_filter = ['tenant', 'rol', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'tenant__name']
    list_editable = ['rol', 'is_active']
    ordering = ['tenant', 'user__username']
    
    def get_queryset(self, request):
        """Filtrar usuarios por tenant"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Aquí implementaremos la lógica de filtrado por tenant
        return qs 