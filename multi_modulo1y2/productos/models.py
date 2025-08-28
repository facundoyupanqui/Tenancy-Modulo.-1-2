from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    """Modelo para manejar diferentes tenants (clínicas, empresas, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Nombre del Tenant")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
    
    def __str__(self):
        return self.name

class Producto(models.Model):
    """Modelo de producto vinculado a un tenant específico"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name="Tenant")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    categoria = models.CharField(max_length=100, verbose_name="Categoría")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        unique_together = ['tenant', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.tenant.name}" 