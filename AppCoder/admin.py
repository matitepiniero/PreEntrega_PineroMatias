from django.contrib import admin
from .models import Cliente, Producto  # Asegúrate de importar Producto aquí

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Producto)  # Registra el modelo Producto aquí
