from django import forms
from .models import Cita, Doctor, Especialidad
from django.utils import timezone
from datetime import date, timedelta

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'fecha', 'hora', 'tipo', 'motivo', 'sintomas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar doctores por tenant del usuario
        if self.user and hasattr(self.user, 'tenant'):
            self.fields['doctor'].queryset = Doctor.objects.filter(
                tenant=self.user.tenant,
                is_active=True
            ).select_related('especialidad')
        
        # Configurar fecha mínima (hoy)
        today = date.today()
        self.fields['fecha'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        
        # Configurar fecha máxima (3 meses)
        max_date = today + timedelta(days=90)
        self.fields['fecha'].widget.attrs['max'] = max_date.strftime('%Y-%m-%d')
        
        # Agregar ayuda
        self.fields['fecha'].help_text = 'Selecciona la fecha para tu cita'
        self.fields['hora'].help_text = 'Selecciona la hora disponible'
        self.fields['tipo'].help_text = 'Tipo de consulta que necesitas'
        self.fields['motivo'].help_text = 'Describe brevemente el motivo de tu consulta'
        self.fields['sintomas'].help_text = 'Describe los síntomas que presentas (opcional)'
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            if fecha < date.today():
                raise forms.ValidationError("No se puede programar una cita en el pasado.")
            if fecha > date.today() + timedelta(days=90):
                raise forms.ValidationError("No se pueden programar citas con más de 3 meses de anticipación.")
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        doctor = cleaned_data.get('doctor')
        
        if fecha and hora and doctor:
            # Verificar que la hora esté dentro del horario del doctor
            if hora < doctor.horario_inicio or hora > doctor.horario_fin:
                raise forms.ValidationError(
                    f"El doctor {doctor.nombre} atiende de {doctor.horario_inicio} a {doctor.horario_fin}"
                )
            
            # Verificar que no haya otra cita en el mismo horario
            if Cita.objects.filter(
                doctor=doctor,
                fecha=fecha,
                hora=hora,
                estado__in=['programada', 'confirmada']
            ).exists():
                raise forms.ValidationError(
                    f"Ya existe una cita programada para el Dr. {doctor.nombre} en {fecha} a las {hora}"
                )
        
        return cleaned_data

class CitaSearchForm(forms.Form):
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha Desde"
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha Hasta"
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Doctor"
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos')] + Cita.ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Estado"
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and hasattr(self.user, 'tenant'):
            self.fields['doctor'].queryset = Doctor.objects.filter(
                tenant=self.user.tenant,
                is_active=True
            ).select_related('especialidad')
