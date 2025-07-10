from django.contrib import admin

from .models import Producto, Categorias,Pedido

@admin.register(Producto)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_producto', 
        'descripcion_producto',
        'precio_producto',
        'cantidad_producto',
        'creacion_producto', 
        'imagen_producto',
        'codigo_producto'
    )
    search_fields = ('nombre_producto', 'descripcion_producto')
    list_filter = ('creacion_producto',)
    readonly_fields = ('codigo_producto',)
    

    # 🛠 Habilitar campos editables en el formulario
    fields = (
        'nombre_producto',
        'descripcion_producto',
        'precio_producto',
        'cantidad_producto',
        'creacion_producto',
        'imagen_producto',
        'id_categoria',
        'codigo_producto'
    )
@admin.register(Categorias)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)
    search_fields = ('nombre_categoria',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin): 
    list_display = ('id_pedido', 'fecha_pedido', 'monto_pedido', 'estado', 'id_usuario')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('id_usuario__nombre_usuario',)


