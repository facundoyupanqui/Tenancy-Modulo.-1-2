from django.db import models
from django.core.exceptions import ValidationError
from productos.models import Tenant
from users.models import CustomUser

class Especialidad(models.Model):
    """Modelo para las especialidades médicas"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='especialidades', verbose_name="Clínica")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Especialidad")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        unique_together = ['tenant', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.tenant.name}"

class Doctor(models.Model):
    """Modelo para los doctores"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='doctores', verbose_name="Clínica")
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='doctores', verbose_name="Especialidad")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Doctor")
    apellido = models.CharField(max_length=100, verbose_name="Apellido del Doctor")
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    horario_inicio = models.TimeField(verbose_name="Hora de Inicio")
    horario_fin = models.TimeField(verbose_name="Hora de Fin")
    dias_laborales = models.CharField(max_length=100, verbose_name="Días Laborales", help_text="Ej: Lunes, Martes, Miércoles")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"
        unique_together = ['tenant', 'email']
    
    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} - {self.especialidad.nombre}"

class Cita(models.Model):
    """Modelo para las citas médicas"""
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_show', 'No Show'),
    ]
    
    TIPO_CHOICES = [
        ('consulta', 'Consulta General'),
        ('control', 'Control'),
        ('emergencia', 'Emergencia'),
        ('seguimiento', 'Seguimiento'),
        ('otro', 'Otro'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='citas', verbose_name="Clínica")
    paciente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='citas_paciente', verbose_name="Paciente")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas_doctor', verbose_name="Doctor")
    fecha = models.DateField(verbose_name="Fecha de la Cita")
    hora = models.TimeField(verbose_name="Hora de la Cita")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='consulta', verbose_name="Tipo de Cita")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada', verbose_name="Estado")
    motivo = models.TextField(verbose_name="Motivo de la Cita")
    sintomas = models.TextField(blank=True, verbose_name="Síntomas")
    notas_medico = models.TextField(blank=True, verbose_name="Notas del Médico")
    diagnostico = models.TextField(blank=True, verbose_name="Diagnóstico")
    tratamiento = models.TextField(blank=True, verbose_name="Tratamiento")
    proxima_cita = models.DateField(null=True, blank=True, verbose_name="Próxima Cita")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        unique_together = ['tenant', 'doctor', 'fecha', 'hora']
        ordering = ['-fecha', '-hora']
    
    def __str__(self):
        return f"Cita de {self.paciente.first_name} {self.paciente.last_name} con Dr. {self.doctor.nombre} - {self.fecha}"
    
    def clean(self):
        # Validar que la fecha no sea en el pasado
        from django.utils import timezone
        from datetime import date
        
        if self.fecha and self.fecha < date.today():
            raise ValidationError("No se puede programar una cita en el pasado.")
        
        # Validar que la hora esté dentro del horario del doctor
        if self.hora and self.doctor:
            if self.hora < self.doctor.horario_inicio or self.hora > self.doctor.horario_fin:
                raise ValidationError(f"La hora debe estar entre {self.doctor.horario_inicio} y {self.doctor.horario_fin}")
    
    @property
    def duracion_estimada(self):
        """Retorna la duración estimada de la cita en minutos"""
        if self.tipo == 'consulta':
            return 30
        elif self.tipo == 'control':
            return 20
        elif self.tipo == 'emergencia':
            return 60
        elif self.tipo == 'seguimiento':
            return 45
        else:
            return 30
