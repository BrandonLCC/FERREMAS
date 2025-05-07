from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto, Categorias, Usuario
from .form import *
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    productos = Producto.objects.select_related().all()[:5]
    return render(request, 'index.html', {'productos':productos} )

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

    context = { 'form' : form }
    return render(request, 'registro_usuario.html',context )


def inicio_sesion(request):
    return render(request, 'inicio_sesion.html', )

