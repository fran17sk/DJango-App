from django import forms
from .models import ProductoPorDeposito

class MovimientoForm(forms.Form):
    MOVIMIENTO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    
    producto_por_deposito = forms.ModelChoiceField(queryset=ProductoPorDeposito.objects.all())
    tipo_movimiento = forms.ChoiceField(choices=MOVIMIENTO_CHOICES)
    cantidad = forms.IntegerField(min_value=1)
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_movimiento = cleaned_data.get("tipo_movimiento")
        cantidad = cleaned_data.get("cantidad")
        producto_por_deposito = cleaned_data.get("producto_por_deposito")

        # Validar que no haya egreso si la cantidad es mayor al stock
        if tipo_movimiento == 'egreso' and producto_por_deposito.cantidad < cantidad:
            self.add_error('cantidad', 'No hay suficiente stock para este egreso.')

        return cleaned_data

