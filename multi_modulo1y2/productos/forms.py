from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        # Excluimos el tenant para que se asigne automáticamente
        exclude = ['tenant']