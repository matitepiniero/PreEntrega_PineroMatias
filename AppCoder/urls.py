from django.urls import *
from AppCoder.views import *
from django.contrib.auth.views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path('logout/', custom_logout, name='logout'),  #  personalizada
    path('crear_perfil/', login_required(UserProfileCreateView.as_view()), name='crear_perfil'),
    path('detalle_perfil/<int:user_id>/', detalle_perfil, name='detalle_perfil'),
    path("padre/", inicio, name="inicio"),
    path("cliente/", cliente, name="Cliente"),
    path("formCliente/", formCliente, name="formCliente"),
    path('formProducto/', formProducto, name='formProducto'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('lista_productos/', lista_productos, name='lista_productos'),
    path('eliminar_cliente/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('editar_cliente/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('cliente/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
    path('editar_producto/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
        # URLs para Movimientos de Stock
    path('detalle_movimiento_stock/<int:movimiento_stock_id>/', detalle_movimiento_stock, name='detalle_movimiento_stock'),
    path('movimientos_stock/', lista_movimientos_stock, name='lista_movimientos_stock'),
    path('crear_movimiento_stock/', crear_movimiento_stock, name='crear_movimiento_stock'),
    path('editar_movimiento_stock/<int:movimiento_stock_id>/', editar_movimiento_stock, name='editar_movimiento_stock'),
    path('eliminar_movimiento_stock/<int:movimiento_stock_id>/', eliminar_movimiento_stock, name='eliminar_movimiento_stock'),
    # URLs para Depósitos
    path('depositos/', lista_depositos, name='lista_depositos'),
    path('crear_deposito/', crear_deposito, name='crear_deposito'),
    path('editar_deposito/<int:deposito_id>/', editar_deposito, name='editar_deposito'),
    path('eliminar_deposito/<int:deposito_id>/', eliminar_deposito, name='eliminar_deposito'),
    path('tipos_movimiento/', lista_tipos_movimiento, name='lista_tipos_movimiento'),
    path('crear_tipo_movimiento/', crear_tipo_movimiento, name='crear_tipo_movimiento'),
   

    

]
