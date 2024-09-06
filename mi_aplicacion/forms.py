from django import forms
from .models import *
    
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['tipo_movimiento', 'motivo', 'fecha']
        widget=forms.Select(attrs={'id': 'tipo_movimiento'})
    def clean(self):
        cleaned_data = super().clean()
        tipo_movimiento = cleaned_data.get('tipo_movimiento')
        motivo = cleaned_data.get('motivo')

        # Validar que el motivo corresponda al tipo de movimiento
        if tipo_movimiento == 'ING' and motivo not in dict(Movement.MOTIVOS_INGRESO_CHOICES):
            self.add_error('motivo', "El motivo seleccionado no es válido para un ingreso.")
        elif tipo_movimiento == 'EGR' and motivo not in dict(Movement.MOTIVOS_EGRESO_CHOICES):
            self.add_error('motivo', "El motivo seleccionado no es válido para un egreso.")

        return cleaned_data

