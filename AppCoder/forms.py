from django import forms
from .models import *
from .models import UserProfile


class formularioCliente(forms.Form):

    nombre=forms.CharField(max_length=30, label='Nombre del Cliente', widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido=forms.CharField(max_length=30, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cel=forms.CharField(max_length=12, label='Numero de Cel', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email=forms.EmailField(label='Correo Elec', widget=forms.TextInput(attrs={'class': 'form-control'}))


class FormularioProductoPersonalizado(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre del Producto', widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo = forms.CharField(max_length=50, label='Código del Producto', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    precio_venta = forms.DecimalField(max_digits=10, decimal_places=2, label='Precio de Venta', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data.get('precio_venta')
        if precio_venta is not None and precio_venta < 0:
            raise forms.ValidationError("El precio de venta no puede ser negativo.")
        return precio_venta

class FormularioEditarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'codigo_barras', 'precio_venta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),  # Agrega este campo
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'codigo': 'Código del Producto',
            'codigo_barras': 'Código de Barras',  # Agrega este label
            'precio_venta': 'Precio de Venta',
        }

class FormularioEditarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'cel']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cel': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Email',
            'cel': 'Cel',
        }

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['producto', 'cantidad', 'deposito', 'tipo_movimiento']  # Incluye los nuevos campos

        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'deposito': forms.Select(attrs={'class': 'form-control'}),
            'tipo_movimiento': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'deposito': 'Depósito',
            'tipo_movimiento': 'Tipo de Movimiento',
        }

class TipoMovimientoForm(forms.ModelForm):
    class Meta:
        model = TipoMovimiento
        fields = ['numero', 'nombre']

class FormularioCrearDeposito(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ['nombre', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del Depósito',
            'direccion': 'Dirección del Depósito',
        }



class FormularioEditarDeposito(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ['nombre', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del Depósito',
            'direccion': 'Dirección del Depósito',
        }

class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ['nombre', 'direccion']

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')

        # Verificar si el nombre del depósito ya existe en la base de datos
        if Deposito.objects.filter(nombre=nombre).exists():
            self.add_error('nombre', 'Este nombre de depósito ya existe en la base de datos.')

        # Puedes agregar más validaciones aquí si es necesario

        return cleaned_data
    
    
class TipoMovimientoForm(forms.ModelForm):
    class Meta:
        model = TipoMovimiento
        fields = ['nombre']

class FormularioMovimientoStock(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['producto', 'tipo_movimiento', 'cantidad', 'deposito', 'fecha']
        exclude = ['fecha']  # Excluye el campo 'fecha' del formulario


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False) 
    class Meta:
        model = UserProfile
        fields = ('avatar',)


    

