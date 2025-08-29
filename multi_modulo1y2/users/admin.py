from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tenant', 'is_active', 'created_at')
    list_filter = ('tenant', 'is_active', 'tipo_sangre', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'tenant__name')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'tenant')
        }),
        ('Información Médica', {
            'fields': ('fecha_nacimiento', 'telefono', 'direccion', 'tipo_sangre', 'alergias', 'condiciones_medicas'),
            'classes': ('collapse',)
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'tenant', 'password1', 'password2'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant=request.user.tenant)
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ('tenant', 'is_superuser', 'is_staff')
        return ()
    
    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)