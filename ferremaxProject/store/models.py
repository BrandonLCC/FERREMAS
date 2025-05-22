import random
import string
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
    nombre_producto = models.CharField(max_length=50)
    descripcion_producto = models.TextField()
    precio_producto = models.IntegerField()
    cantidad_producto = models.IntegerField(default=0)
    creacion_producto = models.DateTimeField(default=timezone.now) 
    imagen_producto = models.ImageField(upload_to='producto/', null=True, blank=True)
    id_categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, default=0)
    codigo_producto = models.CharField(max_length=10, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo_producto:
            self.codigo_producto = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)


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


class Envio(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Envio para {self.carrito.usuario.username} - Costo: {self.costo_envio}"



# metodo de envio
class MetodoEntrega(models.Model):
    OPCIONES_ENVIO = [
        ('domicilio', 'Envío a domicilio'),
        ('tienda', 'Retiro en tienda'),
    ]

    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    tipo_envio = models.CharField(max_length=20, choices=OPCIONES_ENVIO)
    costo = models.PositiveIntegerField(default=0)
    region = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    sede = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.carrito} - {self.get_tipo_envio_display()}"

#Un usuario tiene muchos pedido
#Una pedido tiene un metodo de envio
#una pedido tiene la id detalle compra o carrito 
class Pedido(models.Model): 
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    monto_pedido =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, default='Pendiente')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
   

class detalle_pedido(models.Model): 
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()  
    precio_producto = models.IntegerField()  
    subtotal = models.IntegerField()  
