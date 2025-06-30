from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from .form import *
from django.shortcuts import get_object_or_404
#Importacion de rest
from rest_framework.response import Response
#Importacion webpay
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_api_keys import IntegrationApiKeys #sacada de github
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes  #sacada  del github
from transbank.common.integration_type import IntegrationType #para poder integrar tipo de transaccion test

# Create your views here.
def home(request):
    productos = Producto.objects.select_related('id_categoria').all()[:6]
    
    categoria_basicos = Categorias.objects.get(nombre_categoria='Materiales Básicos')
    catmaterialesBasicos = Producto.objects.filter(id_categoria=categoria_basicos)[:6]
    categoria_seguidad = Categorias.objects.get(nombre_categoria='Equipos de Seguridad')
    catEquiposSeguridad = Producto.objects.filter(id_categoria=categoria_seguidad)[:6]

    user = request.user

    if user.is_active:
        estado = 'usuarioAutenticado'
    else:
        estado = 'false'

    return render(request, 'index.html' ,{'productos': productos,'catmaterialesBasicos': catmaterialesBasicos,'catEquiposSeguridad':catEquiposSeguridad,'estado':estado})

def listaProductos(request):
    user = request.user

    if user.is_active:
        estado = 'usuarioAutenticado'
    else:
        estado = 'false'
    
    categoria = request.GET.get('id_categoria', '')  

    if categoria:
        productos = Producto.objects.filter(id_categoria=categoria).select_related('id_categoria') #filtramos por id de la cate
    else:
        categoria = None
        productos = Producto.objects.all()  

    return render(request, 'lista_productos.html', {'categoria':categoria,'productos':productos,'estado':estado})

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

    user = request.user

    if user.is_active:
        estado = 'usuarioAutenticado'
    else:
        estado = 'false'

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
        'descuento_aplicado': descuento_aplicado,
        'estado':estado
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
                messages.success(request, 'Cantidad actualizada correctamente en el carrito de compra.')
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


def Metodo_envio(request):
   # Asegúrate de que esto retorne un número (no string)
    carrito = get_object_or_404(Carrito, usuario=request.user)
    elementos = ElementoCarrito.objects.filter(carrito=carrito)
    total_carrito = 0
    for elemento in elementos:
        elemento.total = elemento.producto.precio_producto * elemento.cantidad
        total_carrito += elemento.total

    costo_envio = 5000 

    total_con_envio = total_carrito + costo_envio
    
    return render(request, 'metodo_envio.html' , {
                            'elementos': elementos,
                            'total_carrito': total_carrito,
                            'costo_envio': costo_envio,
                            'total_con_envio': total_con_envio,}
                  )


def calcular_total_con_envio(user):
    carrito = get_object_or_404(Carrito, usuario=user)
    elementos = ElementoCarrito.objects.filter(carrito=carrito)
    total_carrito = 0
    for elemento in elementos:
        elemento.total = elemento.producto.precio_producto * elemento.cantidad
        total_carrito += elemento.total

    costo_envio = 5000
    total_con_envio = total_carrito + costo_envio
    return total_con_envio

def seleccionar_metodo_envio(request):
    if request.method == 'POST':
        metodo_envio = request.POST.get('metodo_envio')

        if metodo_envio == '5000':  
            region = request.POST.get('region')
            ciudad = request.POST.get('ciudad')
            direccion = request.POST.get('direccion')
            request.session['envio'] = {
                'tipo': 'domicilio',
                'region': region,
                'ciudad': ciudad,
                'direccion': direccion,
                'costo': 5000,
            }
        else:
            request.session['envio'] = {
                'tipo': 'tienda',
                'direccion': 'sede metropolitana',
                'region': 'metropolitana',
                'costo': 0,
            }

        return redirect('confirmar_pago')  

    return redirect('carrito')  

def Iniciar_pago(request):

    total_con_envio = calcular_total_con_envio(request.user)

    #Codigo integracion, Key test, Modo = test 
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS,
                                    IntegrationApiKeys.WEBPAY, 
                                    IntegrationType.TEST
                                    
                                    ))
    
    
    #Simulacion de datos
    buy_order = "ejemplo100"# Este número debe ser único para cada transacción.
    session_id = "sesionejemplo123" #este valor es devuelto al final de la transacción. 
    amount = total_con_envio #Monto de la transacción. Máximo 2 decimales para USD. 
    #Datos de la orden

    try:
        usuario = Usuario.objects.get(correo_usuario=request.user.email)  
        #Registro del pedido en la base de datos
        pedido_usuario = Pedido.objects.create(
                monto_pedido=amount,
                id_usuario=usuario #en caso de que de error:usuario.id 
            )
        print("Venta pedido realizada:", pedido_usuario)
    
    except ValueError as e:
        print("Error al almacenar el pedido",e)


    try:
        carrito = get_object_or_404(Carrito, usuario=request.user)
        elementos = ElementoCarrito.objects.filter(carrito=carrito)

        for item in elementos:
            Detalle_pedido.objects.create(
                id_pedido=pedido_usuario,
                id_producto=item.producto,
                cantidad_producto=item.cantidad,
                precio_producto=item.producto.precio_producto  
            )


        print("Detalle del pedido creado")

    except Exception as e:
        print("Detalle del pedido no creado", e)


    return_url = "http://127.0.0.1:8000/store/resultado_pago/" #url luego del proceso de pago 
    #Funcion create que recibe los datos de la orden
    resp = tx.create(buy_order, session_id, amount, return_url)

    return redirect(f"{resp['url']}?token_ws={resp['token']}")

#Por ralizar
def Resultado_pago(request):
    #token = request.GET.get("token_ws")
    try:
        pedido = Pedido.objects.select_related('id_usuario').latest('fecha_pedido')
    except Pedido.DoesNotExist:
        pedido = None  # O redirecciona a una vista apropiada, o muestra un mensaje
        # Por ejemplo: return render(request, 'store/error_pedido.html')
    return render(request, 'resultado_pago.html',{"pedido":pedido}) 


def Pedidos_pendientes(request):
    #AQUI MOTRAR TODOS LOS PEDIDOS "IF" TIENEN EL ESTADO DE PENDIENTE
    try:
        usuario = Usuario.objects.get(correo_usuario=request.user.email)
        pedidos = Pedido.objects.filter(id_usuario=usuario, estado='pendiente')
    except Usuario.DoesNotExist:
        pedidos = [] 

    return render(request, 'Pedidos_pendientes.html', {"pedidos":pedidos}) 

##Aqui se vera todos el detalle de los pedidos del usuario
def detalle_pedido(request,pedido_id):
    try:
        usuario = Usuario.objects.get(correo_usuario=request.user.email)
        pedido = get_object_or_404(Pedido, id_pedido=pedido_id, id_usuario=usuario)

        detalles = Detalle_pedido.objects.filter(id_pedido=pedido).select_related('id_producto')

    except Usuario.DoesNotExist:
        detalles = []

    return render(request, 'detalle_pedido.html', {'detalles': detalles})

#historial
def compras_usuario(request):
    try:
        usuario = Usuario.objects.get(correo_usuario=request.user.email)
        ventas = Pedido.objects.filter(id_usuario=usuario, estado='confirmado')
    except Usuario.DoesNotExist:
        ventas = [] 

    return render(request, 'historial_compras.html', {"ventas":ventas}) 

