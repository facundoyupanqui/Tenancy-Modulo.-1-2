from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from productos.models import Tenant

class CustomUser(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users', verbose_name="Clínica", null=True, blank=True)
    
    # Campos médicos
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    tipo_sangre = models.CharField(max_length=5, blank=True, verbose_name="Tipo de Sangre", choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    alergias = models.TextField(blank=True, verbose_name="Alergias")
    condiciones_medicas = models.TextField(blank=True, verbose_name="Condiciones Médicas")
    
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def clean(self):
        # Validar que no se cambie el tenant si ya existe
        if self.pk:
            old_instance = CustomUser.objects.get(pk=self.pk)
            if old_instance.tenant != self.tenant:
                raise ValidationError("No se permite cambiar la clínica de un usuario.")
        super().clean()
    
    def save(self, *args, **kwargs):
        # Validar que el usuario tenga un tenant asignado, excepto para superusuarios
        if not self.pk and self.tenant is None and not self.is_superuser:
            raise ValueError("Un usuario debe estar asociado a una clínica.")
            
        # Validar que no se cambie el tenant
        if self.pk:
            self.clean()
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        if self.tenant:
            return f"{self.username} - {self.tenant.name}"
        return f"{self.username}"
    
    @property
    def edad(self):
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None