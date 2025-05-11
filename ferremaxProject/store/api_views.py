from rest_framework import viewsets
from .models import Producto, Carrito, ElementoCarrito
from .serializers import ProductoSerializer, CarritoSerializer, ElementoCarritoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class ElementoCarritoViewSet(viewsets.ModelViewSet):
    queryset = ElementoCarrito.objects.all()
    serializer_class = ElementoCarritoSerializer
