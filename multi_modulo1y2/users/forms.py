from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from productos.models import Tenant

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'tenant', 'fecha_nacimiento', 'telefono', 'direccion', 'tipo_sangre', 'alergias', 'condiciones_medicas')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar campos con Bootstrap
        for field_name, field in self.fields.items():
            if field_name not in ['tenant']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Hacer campos requeridos
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Agregar ayuda y validación
        self.fields['email'].help_text = 'Ingresa tu dirección de email válida'
        self.fields['first_name'].help_text = 'Ingresa tu nombre'
        self.fields['last_name'].help_text = 'Ingresa tu apellido'
        self.fields['fecha_nacimiento'].help_text = 'Fecha de nacimiento (opcional)'
        self.fields['telefono'].help_text = 'Número de teléfono (opcional)'
        self.fields['direccion'].help_text = 'Dirección de residencia (opcional)'
        self.fields['tipo_sangre'].help_text = 'Tipo de sangre (opcional)'
        self.fields['alergias'].help_text = 'Lista de alergias conocidas (opcional)'
        self.fields['condiciones_medicas'].help_text = 'Condiciones médicas relevantes (opcional)'
        
        # Configurar el campo tenant
        self.fields['tenant'].widget.attrs.update({'class': 'form-select'})
        self.fields['tenant'].help_text = 'Selecciona la clínica a la que perteneces'
        
        # Configurar campos de fecha
        self.fields['fecha_nacimiento'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        )
        
        # Configurar campos de texto largo
        self.fields['direccion'].widget.attrs.update({'rows': 3})
        self.fields['alergias'].widget.attrs.update({'rows': 2})
        self.fields['condiciones_medicas'].widget.attrs.update({'rows': 2})

class UserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'tenant', 'fecha_nacimiento', 'telefono', 'direccion', 'tipo_sangre', 'alergias', 'condiciones_medicas')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar campos con Bootstrap
        for field_name, field in self.fields.items():
            if field_name not in ['tenant']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Configurar el campo tenant
        self.fields['tenant'].widget.attrs.update({'class': 'form-select'})
        
        # Configurar campos de fecha
        self.fields['fecha_nacimiento'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        )
        
        # Configurar campos de texto largo
        self.fields['direccion'].widget.attrs.update({'rows': 3})
        self.fields['alergias'].widget.attrs.update({'rows': 2})
        self.fields['condiciones_medicas'].widget.attrs.update({'rows': 2})