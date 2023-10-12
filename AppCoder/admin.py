from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Producto)  
admin.site.register(Deposito)
admin.site.register(TipoMovimiento)
admin.site.register(MovimientoStock)