
from django.urls import path , include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
#api rest
from rest_framework.routers import DefaultRouter
from .api_views import ProductoViewSet, CarritoViewSet, ElementoCarritoViewSet

#api rest
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'elementos', ElementoCarritoViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro_usuario, name='registro'),
    #Login
    path('inicio_sesion/', LoginView.as_view(template_name='inicio_sesion.html'), name='inicio_sesion'),
    #Logout
    path('cerrar_sesion/', LogoutView.as_view(template_name='cerrar_sesion.html'), name='cerrar_sesion'),
    #Autenticación de usuario
    path('autenticacion/', views.agregar_al_carrito, name='autenticacion'),

    path('productos/', views.listaProductos, name='lista_productos'),
    path('producto/<int:pk>/', views.detalle_productos, name='detalle_productos'),
    #carrito de compra
    path('carro_compra/', views.carro_compra, name='carro_compra'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:elemento_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carro/modificar/<int:elemento_id>/', views.modificar_cantidad_carrito, name='modificar_cantidad_carrito'),
    #Metodo de envio
    path('metodo_envio/', views.Metodo_envio, name='metodo_envio'),
    #Pago
    path('iniciar_pago/', views.Iniciar_pago, name='iniciar_pago'),
    path('resultado_pago/', views.Resultado_pago, name='resultado_pago'),
    #URLs despues del pago
    path('Pedidos_pendientes/', views.Pedidos_pendientes, name='Pedidos_pendientes'),
    path('compras_usuario/', views.Compras_usuario, name='compras_usuario'),

    #api rest
    path('api/', include(router.urls)),
 
]
   # path('inicio_sesion/', LoginView.as_view(template_name='inicio_sesion.html'), name='inicio_sesion'),
 