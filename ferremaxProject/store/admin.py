from django.contrib import admin

from .models import Producto, Categorias

@admin.register(Producto)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_producto', 
        'descripcion_producto',
        'precio_producto',
        'cantidad_producto',
        'creacion_producto', 
        'imagen_producto'
    )
    search_fields = ('nombre_producto', 'descripcion_producto')
    list_filter = ('creacion_producto',)

    # 🛠 Habilitar campos editables en el formulario
    fields = (
        'nombre_producto',
        'descripcion_producto',
        'precio_producto',
        'cantidad_producto',
        'creacion_producto',
        'imagen_producto',
        'id_categoria',
    )
@admin.register(Categorias)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)
    search_fields = ('nombre_categoria',)


