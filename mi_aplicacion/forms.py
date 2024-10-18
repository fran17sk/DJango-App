from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
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


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre de usuario',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
    }))

    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Añadir campo de email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre', 'correo', 'telefono', 'consulta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'consulta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Consulta'}),
        }