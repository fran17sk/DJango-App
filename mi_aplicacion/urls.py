from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/detail/<int:pk>/',ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('sucursales/',SucursalListView.as_view(),name='sucursal_list'),
    path('sucursales/nuevo/',SucursalCreateView.as_view(),name='sucursal_create'),
    path('sucursales/eliminar/<int:pk>',SucursalDeleteView.as_view(),name='sucursal_delete'),
    path('sucursales/editar/<int:pk>',SucursalUpdateView.as_view(),name='sucursal_update'),
    path('sucursales/detail/<int:pk>/',SucursalDetailView.as_view(), name='sucursal_detail'),
    path('depositos/',DepositosListView.as_view(), name='depositos_list'),
    path('depositos/nuevo',DepositoCreateView.as_view(), name='deposito_create'),
    path('depositos/editar/<int:pk>/',DepositoUpdateView.as_view(), name='deposito_update'),
    path('depositos/delete/<int:pk>/',DepositoDeleteView.as_view(), name='deposito_delete'),
    path('depositos/detail/<int:pk>/',DepositoDetailView.as_view(), name='deposito_detail'),

    
    path('facturas/',views.Facturas_list,name='facturas_list'),
    path('get_orden/',views.getDetalleOrden,name='get_orden'),
    path('facturas/new',views.createFactura.as_view(),name='factura_new'),
    path('facturas/detail/<int:pk>',views.detalleFactura,name='facturas_detail'),

    path('compras/OrdenCompra',OrdenCompraView.as_view(),name='orden_compra'),
    path('proveedores/',ProveedorListView.as_view(),name='proveedor_list'),
    path('proveedores/nuevo/',ProveedorCreateView.as_view(),name='proveedor_create'),
    path('proveedores/eliminar/<int:pk>',ProveedorDeleteView.as_view(),name='proveedor_delete'),
    path('proveedores/editar/<int:pk>',ProveedorUpdateView.as_view(),name='proveedor_update'),
    path('get_productos/',views.get_productos,name='get_productos'),
    path('get_precio/',views.get_precio,name='get_precio'),
    path('confirmar_orden/',views.confirmar_orden_compra,name='confirmar_orden_compra'),
    path('get_proveedores/',views.get_proveedores,name='get_proveedores'),
    path('get_depositos/',views.get_depositos,name='get_depositos'),

  
  
    path('productos_list/', ProductoXDepositoListView.as_view(), name='productos_list'),
    path('productos_list/nuevo/', ProductoXDepositoCreateView.as_view(), name='producto_list_create'),
    path('productos_list/detail/<int:pk>/',ProductoXDepositoDetailView.as_view(), name='producto_list_detail'),
    path('productos_list/editar/<int:pk>/', ProductoXDepositoUpdateView.as_view(), name='producto_list_update'),
    path('productos_list/eliminar/<int:pk>/', ProductoXDepositoDeleteView.as_view(), name='producto_list_delete'),
    
    path('depositos/<int:deposito_id>/productos/', views.productos_por_deposito, name='productos_por_deposito'),
    path('sucursales/<int:sucursal_id>/productos/', views.productos_por_sucursal, name='productos_por_sucursal'),


  
    path('registrar_movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('exito/', views.exito, name='exito'),  # Vista para la página de éxito



    ]


###urlpatterns = [
###    path('', ProductoListView.as_view(), name='producto_list'),
###    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
###    path('nuevo/', ProductoCreateView.as_view(), name='producto_create'),
###    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
###    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
###]
