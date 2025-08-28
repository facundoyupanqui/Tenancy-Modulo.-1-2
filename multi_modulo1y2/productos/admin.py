from django.contrib import admin
from django.contrib.auth.models import User
from .models import Tenant, Producto

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tenant', 'precio', 'stock', 'categoria', 'is_active']
    list_filter = ['tenant', 'categoria', 'is_active', 'created_at']
    search_fields = ['nombre', 'descripcion', 'categoria']
    list_editable = ['precio', 'stock', 'is_active']
    ordering = ['tenant', 'nombre']
    
    def get_queryset(self, request):
        """Filtrar productos por tenant del usuario"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Aquí implementaremos la lógica de filtrado por tenant
        return qs
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el tenant al producto"""
        if not change:  # Solo para nuevos productos
            # Aquí implementaremos la lógica para asignar el tenant
            pass
        super().save_model(request, obj, form, change) 