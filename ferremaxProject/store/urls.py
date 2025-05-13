
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.listaProductos, name='lista_productos'),
    path('registro/', views.registro_usuario, name='registro'),
    path('inicio_sesion/', LoginView.as_view(template_name='inicio_sesion.html'), name='inicio_sesion'),
    path('producto/<int:pk>/', views.detalle_productos, name='detalle_productos'),
    #carrito de compra
    path('carro_compra/', views.carro_compra, name='carro_compra'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:elemento_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carro/modificar/<int:elemento_id>/', views.modificar_cantidad_carrito, name='modificar_cantidad_carrito'),
    path('compra_producto', views.Compra_Producto, name='comprar_producto')
]
   # path('inicio_sesion/', LoginView.as_view(template_name='inicio_sesion.html'), name='inicio_sesion'),
