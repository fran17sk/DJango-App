from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.conf.urls.static import static
from django.conf import settings
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

    path ('productos/listaprecios/',PreciosListView.as_view(),name='precios_list'),
    path ('productos/listaprecios/nuevo/',PreciosCreateView.as_view(),name='precios_create'),
    path ('productos/listaprecios/editar/<int:pk>/',PreciosEditView.as_view(),name='precios_update'),
    path ('productos/listaprecios/historial/<int:producto_id>/',views.precios_por_productos,name='precios_historial'),

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
    path('get_productos_sucursal/',views.get_productos_por_sucursal,name='get_productos_sucursal'),
    
    path('get_precio/',views.get_precio,name='get_precio'),

    path('confirmar_orden/',views.confirmar_orden_compra,name='confirmar_orden_compra'),
    path('get_orden_detalles/', views.get_orden_detalles, name='get_orden_detalles'),

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

    path ('clientes/',ClientesListaView.as_view(),name='clientes_list'),
    path ('clientes/new',views.guardar_cliente,name='cliente_new'),

    path ('ventas/',VentasListView.as_view(),name='ventas_list'),
    path ('ventas/new',VentasCreateView.as_view(),name='ventas_new'),
    path('guardar_ventas/',views.guardar_venta,name='guardar_venta'),
    path('ventas/<int:pk>',views.ventas_detalle,name='ventas_detail'),
    path('get_codigo_afip/', views.get_codigo_AFIP, name='get_codigo_afip'),

    
        ## INFORMES ##
    path('generar-informe/', generar_informe, name='generar_informe'),
    path('generar-informe-facturas/', generar_informe_facturas, name='generar_informe_facturas'),
    path('generar-informe-ventas/', generar_informe_ventas, name='generar_informe_ventas'),
    path('tienda/', views.EcommerceHome, name='tienda'),
    path('tienda/articulos', views.ListProducts , name='productos'),
    path('tienda/contacto',views.ContactView , name='contact'),
    path('tienda/login',EcommerceLoginView, name='ecommerce_login'),
    path('logout_ecomerce/', views.custom_logout_view, name='logout_ecommerce'),
    path('tienda/mi_cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('tienda/logout' , views.custom_logout_view,name='logout_tienda'),
    path('tienda/productos',views.admin_productos,name='admin_prods'),
    path('tienda/productos/<int:pk>',views.admin_producto_edit,name='admin_prods_edit'),
    path('tienda/listar_ventas', views.listar_ventas,name='admin_list_ventas'),
    path('tienda/listar_ventas_entregadas', views.listar_ventas_entregadas,name='admin_list_ventas_entregadas'),
    path('tienda/listar_ventas_pendientes', views.listar_ventas_pendientes,name='admin_list_ventas_pendientes'),
    path('tienda/listar_ventas_despachadas', views.listar_ventas_despachadas,name='admin_list_ventas_despachadas'),
    path('tienda/listar_ventas_preparacion', views.listar_ventas_preparacion,name='admin_list_ventas_preparacion'),

    path('cambiar_estado/<int:orden_id>/', cambiar_estado, name='cambiar_estado'),

    path('producto/<int:producto_id>/agregar_imagenes/', agregar_imagenes, name='agregar_imagenes'),
    path('producto/<int:producto_id>/eliminar_imagen/<int:media_id>/', eliminar_imagen, name='eliminar_imagen'),
    path('tienda/mis_ordenes', views.mis_ordenes, name='mis_ordenes'),
    path('mis-ordenes/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('tienda/nosotros' ,views.nosotros , name='nosotros'),
    path('consulta/responder', views.responder_consultas, name='hola'),
    path('consultas',views.admin_consultas,name='admin_consultas'),
    path('ingresos-egresos/', views.ingresos_egresos_view, name='ingresos_egresos'),
    path('marca-mas-vendida/', views.marca_mas_vendida, name='marca_mas_vendida'),
    path('categoria-mas-vendida/', views.categoria_mas_vendida, name='categoria_mas_vendida'),
    path('empleado-mas-vendio/', views.empleado_mas_vendio, name='empleado_mas_vendio'),
    path('ventas-online/',views.ventas_online,name='ventas_online'),
    path('productos-mas-vendidos/',views.productos_mas_vendidos,name='producto_mas_vendido'),


    path('api/products/', views.get_products_json, name='get_products_json'),
    path('checkout',views.checkout , name='checkout'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


###urlpatterns = [
###    path('', ProductoListView.as_view(), name='producto_list'),
###    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
###    path('nuevo/', ProductoCreateView.as_view(), name='producto_create'),
###    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
###    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
###]
