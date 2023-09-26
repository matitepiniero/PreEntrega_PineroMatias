from django.shortcuts import *
from django.http import HttpResponse
from .forms import *
from AppCoder.models import *

# Create your views here.
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




def lista_productos(request):
    # Obtén el valor de búsqueda desde la URL
    search_query = request.GET.get('search', '')

    # Filtra los productos que coincidan con la búsqueda
    productos = Producto.objects.filter(nombre__icontains=search_query)

    return render(request, 'AppCoder/lista_productos.html', {'productos': productos, 'search_query': search_query})



def detalle_producto(request, producto_id):
    # Obtiene el producto específico según su ID o muestra un error 404 si no existe
    producto = get_object_or_404(Producto, pk=producto_id)
    
    return render(request, 'AppCoder/detalle_producto.html', {'producto': producto})

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

            return render(request, "AppCoder/Inicio.html")
    else:
        formulario = formularioCliente()  # Crea una instancia vacía del formulario

    return render(request, "AppCoder/formCliente.html", {"form1": formulario})


def lista_clientes(request):
    query = request.GET.get('search')
    if query:
        # Filtrar los clientes por nombre si se proporciona una consulta de búsqueda
        clientes = Cliente.objects.filter(nombre__icontains=query)
    else:
        # Si no hay consulta de búsqueda, obtener todos los clientes
        clientes = Cliente.objects.all()
    
    return render(request, 'AppCoder/cliente.html', {'clientes': clientes})

def eliminar_cliente(request, cliente_id):
    # Buscar el cliente por su ID o mostrar un error 404 si no existe
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        # Si se envió una solicitud POST, elimina el cliente
        cliente.delete()
        return redirect('Cliente')  # Redirige a la página de clientes después de eliminar

    # Si la solicitud no es POST (por ejemplo, GET), muestra una confirmación de eliminación
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})
