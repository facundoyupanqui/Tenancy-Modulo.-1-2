from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono', 'tenant', 'created_at')
    list_filter = ('tenant',)
    search_fields = ('nombre', 'apellido', 'email')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        # Filtrar clientes por el tenant del usuario administrador si no es superusuario
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