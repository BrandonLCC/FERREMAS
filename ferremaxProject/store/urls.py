
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.listaProductos, name='lista_productos'),
    path('producto/<int:pk>/', views.detalle_productos, name='detalle_productos'),
    path('registro/', views.registro_usuario, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    #carrito de compra
    path('carro_compra/', views.carro_compra, name='carro_compra'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:elemento_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carro/modificar/<int:elemento_id>/', views.modificar_cantidad_carrito, name='modificar_cantidad_carrito'),
]
