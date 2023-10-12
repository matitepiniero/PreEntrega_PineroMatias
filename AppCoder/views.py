from django.shortcuts import *
from django.http import HttpResponse
from .forms import *
from AppCoder.models import *
from django.contrib.auth import *
import os
import barcode
from barcode.writer import ImageWriter
from django.views.decorators.http import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import View, UpdateView
from .models import UserProfile
from .forms import UserProfileForm
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import FormularioProductoPersonalizado
from .models import Producto

class UserProfileCreateView(View):
    template_name = 'AppCoder/crear_perfil.html'

    def get(self, request, *args, **kwargs):
        # Verificar si el perfil de usuario ya existe
        if UserProfile.objects.filter(user=request.user).exists():
            # Redirigir al usuario a la página de detalle de perfil o donde sea necesario
            return redirect(reverse('detalle_perfil', args=[request.user.id]))

        # Agregar el formulario al contexto
        form1 = UserProfileForm()
        return render(request, self.template_name, {'form1': form1})

    def post(self, request, *args, **kwargs):
        # Verificar si el perfil de usuario ya existe
        if UserProfile.objects.filter(user=request.user).exists():
            # Redirigir al usuario a la página de detalle de perfil o donde sea necesario
            return redirect(reverse('detalle_perfil', args=[request.user.id]))

        form1 = UserProfileForm(request.POST, request.FILES)
        if form1.is_valid():
            # Configurar el usuario asociado al perfil de usuario
            form1.instance.user = request.user
            form1.save()  # Guardar el perfil de usuario
            # Configura la URL de éxito después de guardar el perfil
            success_url = reverse('detalle_perfil', args=[request.user.id])
            return redirect(success_url)
        else:
            # Realizar acciones si el formulario no es válido
            return render(request, self.template_name, {'form1': form1})
        
def detalle_perfil(request, user_id):
    # Obtener el perfil del usuario o mostrar un error 404 si no existe
    user = get_object_or_404(User, id=user_id)
    perfil = UserProfile.objects.get(user=user)

    # Luego, pasa 'perfil' a tu plantilla para mostrar la información del perfil
    return render(request, 'AppCoder/detalle_perfil.html', {'perfil': perfil})
 

def custom_logout(request):
    logout(request)
    return render(request, 'AppCoder/logout.html')

def inicio(request):

    return render(request,"AppCoder/inicio.html")



def cliente(request):
    clientes = Cliente.objects.all()

    # Obtén el valor de búsqueda desde la consulta GET
    search_query = request.GET.get('search')
    if search_query:
        # Filtra los clientes por nombre si se proporciona una consulta de búsqueda
        clientes = clientes.filter(nombre__icontains=search_query)

    return render(request, 'AppCoder/cliente.html', {'clientes': clientes})




def formProducto(request):
    if request.method == "POST":
        formulario = FormularioProductoPersonalizado(request.POST)
        if formulario.is_valid():
            datos_producto = formulario.cleaned_data

            # Verifica si el código ya existe en la base de datos
            if Producto.objects.filter(codigo=datos_producto["codigo"]).exists():
                formulario.add_error("codigo", "Este código ya está en uso.")
            else:
                # Crea una instancia del producto y guárdala en la base de datos
                producto = Producto(
                    nombre=datos_producto["nombre"],
                    codigo=datos_producto["codigo"],
                    precio_venta=datos_producto["precio_venta"]
                )
                producto.save()

                return redirect("detalle_producto", producto_id=producto.id)
    else:
        formulario = FormularioProductoPersonalizado()

    return render(request, "AppCoder/formProducto.html", {"form1": formulario})


def eliminar_producto(request, producto_id):
    # Obtiene el producto específico según su ID o muestra un error 404 si no existe
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        # Si se envió una solicitud POST, elimina el producto
        producto.delete()
        return redirect('lista_productos')  # Redirige a la página de lista de productos después de eliminar

    # Si la solicitud no es POST (por ejemplo, GET), muestra una confirmación de eliminación
    return render(request, 'AppCoder/eliminar_producto.html', {'producto': producto})


def lista_productos(request):
    # Obtén el valor de búsqueda desde la URL
    search_query = request.GET.get('search', '')

    # Filtra los productos que coincidan con la búsqueda
    productos = Producto.objects.filter(nombre__icontains=search_query)

    return render(request, 'AppCoder/lista_productos.html', {'productos': productos, 'search_query': search_query})


def editar_producto(request, producto_id):
    # Obtén el producto específico según su ID o muestra un error 404 si no existe
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == "POST":
        formulario = FormularioEditarProducto(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect("detalle_producto", producto_id=producto.id)
    else:
        formulario = FormularioEditarProducto(instance=producto)

    return render(request, "AppCoder/editar_producto.html", {"formulario": formulario, "producto": producto})


def detalle_producto(request, producto_id):
    # Obtiene el producto específico según su ID o muestra un error 404 si no existe
    producto = get_object_or_404(Producto, pk=producto_id)
    
    return render(request, 'AppCoder/detalle_producto.html', {'producto': producto})


def generar_codigo_de_barras(producto):
    # Ruta donde deseas almacenar las imágenes de códigos de barras
    directorio_imagenes = 'path/C:/PONUS/ProductoIMG/'

    # Verificar si el directorio existe, y si no, crearlo
    if not os.path.exists(directorio_imagenes):
        os.makedirs(directorio_imagenes)

    # Crear un objeto de código de barras (por ejemplo, EAN-13)
    codigo = barcode.get_barcode_class('ean13')

    # Generar el código de barras con el valor del campo 'codigo_barras' del producto
    codigo_generado = codigo(producto.codigo_barras, writer=ImageWriter(), add_checksum=False)

    # Construir la ruta completa para la imagen del código de barras
    ruta_imagen = os.path.join(directorio_imagenes, f'{producto.codigo_barras}.png')

    # Guardar la imagen del código de barras en la ruta
    codigo_generado.save(ruta_imagen)

    return ruta_imagen



def lista_tipos_movimiento(request):
    tipos_movimiento = TipoMovimiento.objects.all()
    return render(request, 'lista_tipos_movimiento.html', {'tipos_movimiento': tipos_movimiento})

def crear_tipo_movimiento(request):
    if request.method == 'POST':
        form = TipoMovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipos_movimiento')
    else:
        form = TipoMovimientoForm()
    return render(request, 'crear_tipo_movimiento.html', {'form': form})

# Vistas para Movimientos de Stock

def lista_movimientos_stock(request):
    # Obtén todos los movimientos de stock
    movimientos_stock = MovimientoStock.objects.all()

    return render(request, 'AppCoder/lista_movimientos_stock.html', {'movimientos_stock': movimientos_stock})

from .models import Producto  # Asegúrate de importar el modelo Producto

def crear_movimiento_stock(request):
    if request.method == 'POST':
        formulario = FormularioMovimientoStock(request.POST)
        if formulario.is_valid():
            movimiento_stock = formulario.save()
            return redirect('lista_movimientos_stock')
    else:
        formulario = FormularioMovimientoStock()
    
    # Obtén la lista de productos y pásala al contexto
    productos = Producto.objects.all()  # Esto obtendrá todos los productos en la base de datos

    return render(request, 'AppCoder/crear_movimiento_stock.html', {'formulario': formulario, 'productos': productos})

def editar_movimiento_stock(request, movimiento_stock_id):
    # Obtén el movimiento de stock específico según su ID o muestra un error 404 si no existe
    movimiento_stock = get_object_or_404(MovimientoStock, pk=movimiento_stock_id)

    if request.method == "POST":
        # Si se envió una solicitud POST, procesa el formulario
        formulario = MovimientoStockForm(request.POST, instance=movimiento_stock)
        if formulario.is_valid():
            formulario.save()
            return redirect('detalle_movimiento_stock', movimiento_stock_id=movimiento_stock.id)
    else:
        # Si la solicitud no es POST, muestra el formulario de edición
        formulario = MovimientoStockForm(instance=movimiento_stock)

    return render(request, 'AppCoder/editar_movimiento_stock.html', {'formulario': formulario, 'movimiento_stock': movimiento_stock})


def detalle_movimiento_stock(request, movimiento_stock_id):
    # Obtiene el movimiento de stock específico según su ID o muestra un error 404 si no existe
    movimiento_stock = get_object_or_404(MovimientoStock, pk=movimiento_stock_id)

    if request.method == 'POST':
        # Si se envió una solicitud POST, elimina el movimiento de stock
        movimiento_stock.delete()
        return redirect('lista_movimientos_stock')  # Redirige a la página de lista de movimientos de stock después de eliminar

    return render(request, 'AppCoder/detalle_movimiento_stock.html', {'movimiento_stock': movimiento_stock})

def eliminar_movimiento_stock(request, movimiento_stock_id):
    # Obtén el movimiento de stock específico según su ID o muestra un error 404 si no existe
    movimiento_stock = get_object_or_404(MovimientoStock, pk=movimiento_stock_id)

    if request.method == 'POST':
        # Si se envió una solicitud POST, elimina el movimiento de stock
        movimiento_stock.delete()
        return redirect('lista_movimientos_stock')  # Redirige a la página de lista de movimientos de stock después de eliminar

    return render(request, 'AppCoder/eliminar_movimiento_stock.html', {'movimiento_stock': movimiento_stock})

def lista_depositos(request):
    # Obtiene todos los depósitos de mercadería
    depositos = Deposito.objects.all()

    return render(request, 'AppCoder/lista_depositos.html', {'depositos': depositos})


def crear_deposito(request):
    if request.method == "POST":
        formulario = FormularioCrearDeposito(request.POST)
        if formulario.is_valid():
            datos_deposito = formulario.cleaned_data

            # Crea una instancia de Deposito y guárdala en la base de datos
            deposito = Deposito(
                nombre=datos_deposito["nombre"],
                direccion=datos_deposito["direccion"]
            )
            deposito.save()

            # Agrega un mensaje de éxito
            messages.success(request, 'Depósito creado con éxito.')

            return redirect("lista_depositos")  # Redirige a la lista de depósitos después de crear uno nuevo

    else:
        formulario = FormularioCrearDeposito()

    return render(request, "AppCoder/crear_deposito.html", {"formulario": formulario})


def editar_deposito(request, deposito_id):
    # Obtiene el depósito específico según su ID o muestra un error 404 si no existe
    deposito = get_object_or_404(Deposito, pk=deposito_id)

    if request.method == "POST":
        formulario = FormularioEditarDeposito(request.POST, instance=deposito)
        if formulario.is_valid():
            formulario.save()
            return redirect("lista_depositos")  # Redirige a la lista de depósitos después de editar
    else:
        formulario = FormularioEditarDeposito(instance=deposito)

    return render(request, "AppCoder/editar_deposito.html", {"formulario": formulario, "deposito": deposito})

@require_POST
def eliminar_deposito(request, deposito_id):
    # Obtiene el depósito específico según su ID o muestra un error 404 si no existe
    deposito = get_object_or_404(Deposito, pk=deposito_id)

    if 'confirmar' in request.POST:
        # Si se envió una solicitud POST con 'confirmar', elimina el depósito
        deposito.delete()
        return redirect('lista_depositos')  # Redirige a la lista de depósitos después de eliminar

    # Si la solicitud es POST sin 'confirmar' (mostrar la página de confirmación) o GET, muestra la página de confirmación
    return render(request, 'AppCoder/confirmar_eliminar_deposito.html', {'deposito': deposito})


def formCliente(request):
    if request.method == "POST":
        formulario = formularioCliente(request.POST)  # Utiliza el nombre correcto del formulario

        if formulario.is_valid():
            info = formulario.cleaned_data

            cliente = Cliente(
                nombre=info["nombre"],
                apellido=info["apellido"],
                cel=info["cel"],
                email=info["email"]
            )
            cliente.save()

            return redirect("detalle_cliente", cliente_id=cliente.id)
    else:
        formulario = formularioCliente()  # Crea una instancia vacía del formulario

    return render(request, "AppCoder/formCliente.html", {"form1": formulario})


def lista_clientes(request):
    # Obtiene el valor de búsqueda de la URL
    search_query = request.GET.get('search', '')

    if search_query:
        # Filtra los clientes que coincidan con el término de búsqueda
        clientes = Cliente.objects.filter(nombre__icontains=search_query)
    else:
        # Si no se proporciona un término de búsqueda, obtener todos los clientes
        clientes = Cliente.objects.all()
    
    return render(request, 'AppCoder/cliente.html', {'clientes': clientes, 'search_query': search_query})


def eliminar_cliente(request, cliente_id):
    # Buscar el cliente por su ID o mostrar un error 404 si no existe
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        # Si se envió una solicitud POST, elimina el cliente
        cliente.delete()
        return redirect('Cliente')  # Redirige a la página de clientes después de eliminar

    # Si la solicitud no es POST (por ejemplo, GET), muestra una confirmación de eliminación
    return render(request, 'AppCoder/eliminar_cliente.html', {'cliente': cliente})


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == "POST":
        formulario = FormularioEditarCliente(request.POST, instance=cliente)
        if formulario.is_valid():
            formulario.save()
            return redirect("detalle_cliente", cliente_id=cliente.id)
    else:
        formulario = FormularioEditarCliente(instance=cliente)

    return render(request, "AppCoder/editar_cliente.html", {"formulario": formulario, "cliente": cliente})

def detalle_cliente(request, cliente_id):
    # Obtén el cliente específico según su ID o muestra un error 404 si no existe
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    return render(request, 'AppCoder/detalle_cliente.html', {'cliente': cliente})

