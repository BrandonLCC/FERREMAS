
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.listaProductos, name='lista_productos'),
    path('producto/<int:pk>/', views.detalle_productos, name='detalle_productos'),
    path('registro/', views.registro_usuario, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),

]
