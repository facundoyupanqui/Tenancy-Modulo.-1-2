from django.db import models
from productos.models import Tenant

class Cliente(models.Model):
    """Modelo de cliente vinculado a un tenant específico"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name="Tenant", related_name='clientes')
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    apellido = models.CharField(max_length=200, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        unique_together = ['tenant', 'email']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.tenant.name}"