from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto, Categorias, Usuario ,Carrito, ElementoCarrito
 
from django.contrib.auth.decorators import login_required
from .form import *
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    productos = Producto.objects.select_related('id_categoria').all()[:6]
    
    user = request.user

    if user.is_active:
        estado = 'usuarioAutenticado'
    else:
        estado = 'false'

    return render(request, 'index.html' ,{'productos': productos,'estado':estado})

def listaProductos(request):
    categoria = request.GET.get('id_categoria', '')  

    if categoria:
        productos = Producto.objects.filter(id_categoria=categoria).select_related('id_categoria') #filtramos por id de la cate
    else:
        categoria = None
        productos = Producto.objects.all()  

    return render(request, 'lista_productos.html', {'categoria':categoria,'productos':productos})

def detalle_productos(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('id_categoria').all(), pk=pk)  

    return render(request, 'detalle_producto.html', {'producto': producto})

def carro_compra(request):
    return render(request, 'carro_compra.html')

def carro_compra(request):
    return render(request, 'carro_compra.html')


def agregar_al_carrito(request, producto_id):
    productos = get_object_or_404(Producto, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = CantidadProductoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            if cantidad > productos.cantidad_producto:  
                form.add_error('cantidad', 'La cantidad solicitada excede el stock disponible.')
            else:
                elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=productos)

                if not creado:
                    elemento.cantidad += cantidad
                else:
                    elemento.cantidad = cantidad

                elemento.save()

                Producto.objects.filter(id=productos.id).update(
                    cantidad_producto=productos.cantidad_producto - cantidad
                )

                return redirect('carro_compra')
    else:
        form = CantidadProductoForm()

    return render(request, 'detalle_producto.html', {'producto': productos, 'form': form})

@login_required
def carro_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    elementos = ElementoCarrito.objects.filter(carrito=carrito)
    
    total_carrito = 0
    for elemento in elementos:
        elemento.total = elemento.producto.precio_producto * elemento.cantidad
        total_carrito += elemento.total

    descuento_aplicado = 0
    total_carrito_con_descuento = total_carrito

    if request.method == 'POST':
        codigo_descuento = request.POST.get('codigo_descuento', '').strip()
        if codigo_descuento == 'DESCUENTO10':  
            descuento_aplicado = 10  
            total_carrito_con_descuento = total_carrito - (total_carrito * descuento_aplicado / 100)
        elif codigo_descuento == 'DESCUENTO20':
            descuento_aplicado = 20  
            total_carrito_con_descuento = total_carrito - (total_carrito * descuento_aplicado / 100)

    request.session['descuento_aplicado'] = descuento_aplicado
    request.session['total_carrito_con_descuento'] = total_carrito_con_descuento

    return render(request, 'carro_compra.html', {
        'elementos': elementos,
        'total_carrito': total_carrito,
        'total_carrito_con_descuento': total_carrito_con_descuento,
        'descuento_aplicado': descuento_aplicado
    })

def eliminar_del_carrito(request, elemento_id):
    elemento = get_object_or_404(ElementoCarrito, id=elemento_id)
    elemento.delete()
    return redirect('carro_compra')


#agregar modificar cantidad de stock producto

def modificar_cantidad_carrito(request, elemento_id):
    elemento = get_object_or_404(ElementoCarrito, id=elemento_id)
    if request.method == 'POST':
        form = CantidadProductoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            if cantidad > elemento.producto.cantidad_producto:
                messages.error(request, 'La cantidad solicitada excede el stock disponible.')
            else:
                elemento.cantidad = cantidad
                elemento.save()
                messages.success(request, 'Cantidad actualizada correctamente.')
                return redirect('carro_compra')
    else:
        form = CantidadProductoForm(initial={'cantidad': elemento.cantidad})

    return redirect('carro_compra')






def registro_usuario(request):
    if request.method == 'POST':
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password2 = form.cleaned_data['password2']
                form.save()  # Guarda usuario 
                usuario = Usuario.objects.create(
                    nombre_usuario = username,
                    correo_usuario = email,
                    contraseña_usuario = password2,

                )
                messages.success(request, f"El usuario:{username} ha sido creado")
                return redirect('home')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html',{ 'form' : form } )
