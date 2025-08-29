from django.contrib import admin
from .models import Producto, Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'phone_number', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'address', 'phone_number')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        # Solo superusuarios pueden ver todos los tenants
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Usuarios normales solo ven su propio tenant
        if hasattr(request.user, 'tenant') and request.user.tenant:
            return qs.filter(id=request.user.tenant.id)
        return qs.none()

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'tenant', 'created_at')
    list_filter = ('tenant',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        # Filtrar productos por el tenant del usuario administrador si no es superusuario
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant=request.user.tenant)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limitar la selección de tenant al tenant del usuario si no es superusuario
        if db_field.name == "tenant" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.tenant.__class__.objects.filter(id=request.user.tenant.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el tenant del usuario si no se ha especificado
        if not obj.tenant and not request.user.is_superuser:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)