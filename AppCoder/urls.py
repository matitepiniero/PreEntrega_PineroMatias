from django.urls import *
from AppCoder.views import *

urlpatterns = [
    path("", inicio, name="Inicio"),
    path("cliente/", cliente, name="Cliente"),
    path("formCliente/", formCliente, name="formCliente"),
    path('formProducto/', formProducto, name='formProducto'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('lista_productos/', lista_productos, name='lista_productos'),
    path('eliminar_cliente/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
    path('clientes/', lista_clientes, name='lista_clientes'),
]
