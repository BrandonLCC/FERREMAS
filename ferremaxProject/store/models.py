from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Categorias(models.Model):
    id_categoria = models.IntegerField(primary_key=True) 
    nombre_categoria = models.CharField(max_length = 50)
    imagen_categoria = models.ImageField(upload_to='categoria/', null=True, blank=True)

    def __str__(self):
        return self.nombre_categoria    

class Producto(models.Model):
    nombre_producto = models.CharField(max_length = 50)
    descripcion_producto = models.TextField()
    precio_producto = models.IntegerField()
    cantidad_producto = models.IntegerField(default=0)  
    creacion_producto = models.DateTimeField(auto_now_add=True)
    imagen_producto = models.ImageField(upload_to='producto/', null=True, blank=True)
    id_categoria = models.ForeignKey(Categorias,on_delete=models.CASCADE, default=0)#Sin categoria
    #id_almacen = models.ForeignKey(Almacenes, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre_producto    

class Usuario(models.Model):
    nombre_usuario =  models.CharField(max_length=100)
    correo_usuario = models.CharField(max_length=100)
    contraseña_usuario = models.CharField(max_length=100)


class Carrito(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
 
class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
 
    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.cantidad} unidades"
    
class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

