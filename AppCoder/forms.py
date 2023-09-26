from django import forms

class formularioCliente(forms.Form):

    nombre=forms.CharField(max_length=30)
    apellido=forms.CharField(max_length=30)
    cel=forms.CharField(max_length=12)
    email=forms.EmailField()

class FormularioProductoPersonalizado(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre del Producto', widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo = forms.CharField(max_length=50, label='Código del Producto', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    precio_venta = forms.DecimalField(max_digits=10, decimal_places=2, label='Precio de Venta', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data.get('precio_venta')
        if precio_venta is not None and precio_venta < 0:
            raise forms.ValidationError("El precio de venta no puede ser negativo.")
        return precio_venta

