
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lista_productos/', views.listaProductos, name='listaProductos'),

]
