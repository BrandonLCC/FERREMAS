from django.shortcuts import render, redirect
from .models import Producto, Categorias

# Create your views here.
def home(request):
    productos = Producto.objects.select_related().all()[:5]
    return render(request, 'index.html', {'productos':productos} )

def listaProductos(request):
    return 0

'''


def listaProductos(request):
      categoria = request.GET.get('id_categoria', '')  

    if categoria:
        productos = Producto.objects.filter(id_categoria=categoria).select_related('id_categoria') #filtramos por id de la cate
    else:
        categoria = None
        productos = Producto.objects.all()  

    return render(request, 'listaProductos.html', {'categoria':categoria,'productos':productos} )
    '''