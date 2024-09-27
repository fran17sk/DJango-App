from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('productos/', views.ProductoListView, name='producto_list'),
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
    path('registrar_factura',views.registrar_factura,name='registrar_factura'),

    path('compras/OrdenCompra',OrdenCompraView.as_view(),name='orden_compra'),
    path('compras/',OrdenCompraListView.as_view(),name='orden_list'),
    path('compras/detail/<int:pk>',views.detalleorden,name='orden_detail'),
    path('get_ordenes/',views.get_ordenes,name='get_ordenes'),

    path ('pagos/',views.pagos_list,name='pagos_list'),
    path ('pagos/nuevo',PagoCreateView.as_view(),name='pago_new'),
    path ('pagos/detail/<int:pk>',views.pago_detail,name='pago_detail'),
    path ('get_facturas/',views.get_facturas,name='get_facturas'),
    path('registrar_pago/',views.registrar_pago,name='registrar_pago'),

    path('proveedores/',ProveedorListView.as_view(),name='proveedor_list'),
    path('proveedores/nuevo/',ProveedorCreateView.as_view(),name='proveedor_create'),
    path('proveedores/eliminar/<int:pk>',ProveedorDeleteView.as_view(),name='proveedor_delete'),
    path('proveedores/editar/<int:pk>',ProveedorUpdateView.as_view(),name='proveedor_update'),
    path('get_productos/',views.get_productos,name='get_productos'),

    path('get_productos_deposito/',views.get_productos_por_deposito,name='get_productos_deposito'),
    
    path('get_precio/',views.get_precio,name='get_precio'),

    path('confirmar_orden/',views.confirmar_orden_compra,name='confirmar_orden_compra'),
    path('get_proveedores/',views.get_proveedores,name='get_proveedores'),
    path('get_depositos/',views.get_depositos,name='get_depositos'),

    path('categorias/',CategoriaListView.as_view(),name='categoria_list'),
    path('categorias/nuevo/',CategoriaCreateView.as_view(),name='categoria_create'),
    path('categorias/eliminar/<int:pk>',CategoriaDeleteView.as_view(),name='categoria_delete'),
    path('categorias/editar/<int:pk>',CategoriaUpdateView.as_view(),name='categoria_update'),
  
  
  
    path('productos_list/', ProductoXDepositoListView.as_view(), name='productos_list'),
    path('productos_list/nuevo/', ProductoXDepositoCreateView.as_view(), name='producto_list_create'),
    path('productos_list/detail/<int:pk>/',ProductoXDepositoDetailView.as_view(), name='producto_list_detail'),
    path('productos_list/editar/<int:pk>/', ProductoXDepositoUpdateView.as_view(), name='producto_list_update'),
    path('productos_list/eliminar/<int:pk>/', ProductoXDepositoDeleteView.as_view(), name='producto_list_delete'),
    
    path('depositos/<int:deposito_id>/productos/', views.productos_por_deposito, name='productos_por_deposito'),
    path('sucursales/<int:sucursal_id>/productos/', views.productos_por_sucursal, name='productos_por_sucursal'),

    path('movimiento/<int:movimiento_id>' , views.movimientos_detail_view,name='movimiento_detail'),
    path('depositos/<int:deposito_id>/list',views.movimientos_list_view,name='movimientos_list'),
    path('depositos/<int:deposito_id>/registar-movimiento/', views.registrar_movimiento_form, name='registrar_movimiento'),
    path('depositos/registar-movimiento/', views.registrar_movimiento, name='registrar_mov'),
    path('exito/', views.exito, name='exito'),  # Vista para la página de éxito



    path('tienda/', views.EcommerceHome, name='tienda'),
    path('tienda/articulos', views.ListProducts , name='productos'),
    path('tienda/contacto',ContactView.as_view() , name='contact'),
    path('tienda/login',EcommerceLoginView, name='ecommerce_login'),
    path('logout_ecomerce/', views.custom_logout_view, name='logout_ecommerce'),
    path('tienda/mi_cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('tienda/logout' , views.custom_logout_view,name='logout_tienda'),


    path('api/products/', views.get_products_json, name='get_products_json'),
    path('checkout',views.checkout , name='checkout'),
    ]


###urlpatterns = [
###    path('', ProductoListView.as_view(), name='producto_list'),
###    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
###    path('nuevo/', ProductoCreateView.as_view(), name='producto_create'),
###    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
###    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
###]
