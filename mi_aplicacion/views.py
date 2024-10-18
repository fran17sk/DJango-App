from django.http import JsonResponse
from django.contrib.auth.models import Group
from .models import Producto
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
import json
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomLoginForm
from django.db.models import Sum,Count,F
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
import matplotlib
matplotlib.use('Agg')  # Configurar backend no interactivo
import matplotlib.pyplot as plt
import io
from .utils import obtener_latitud_longitud  
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Cast
from django.db import connection

@login_required
def home(request):
    return render(request, 'base.html')

def ProductoListView(request):
    cat = request.GET.get('category')
    user = request.user
    if cat:
        category = Categoria.objects.get(id=cat)
        productos = Producto.objects.filter(categoria=category)
    else: 
        productos = Producto.objects.all()
    return render(request,'productos/producto_list.html',{'productos':productos,'user': user})
 

################################PRODUCTOS########################################

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion','categoria','estado','proveedor']
    success_url = reverse_lazy('producto_list')
    

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion','categoria','estado']
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')


################################LISTA DE PRECIOS########################################
class PreciosListView(LoginRequiredMixin,ListView):
    model = ListaPrecio
    template_name='productos/Precios/precios_list.html'
    context_object_name='listaprecio'
    login_url='../accounts/login'

class PreciosCreateView(CreateView):
    model = ListaPrecio
    fields = ['producto', 'precio', 'fecha_creacion']
    template_name = 'productos/Precios/precios_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Consulta de productos que no están en ListaPrecio
        productos_sin_precio = Producto.objects.exclude(id__in=ListaPrecio.objects.values('producto_id'))
        context['productos_sin_precio'] = productos_sin_precio
        return context
    def form_valid(self, form):
        # Guardar el nuevo precio y agregar la entrada en HistorialPrecio
        response = super().form_valid(form)

        # Crear la entrada en HistorialPrecio
        HistorialPrecio.objects.create(
            producto=form.instance.producto,
            precio_anterior=form.instance.precio,
            fecha_modificacion=form.instance.fecha_creacion
        )
        return response
    success_url=reverse_lazy('precios_list')

class PreciosEditView(UpdateView):
    model = ListaPrecio
    fields=['producto','precio','fecha_creacion']
    template_name='productos/Precios/precios_update.html'
    def form_valid(self, form):
        # Guardar el nuevo precio y agregar la entrada en HistorialPrecio
        response = super().form_valid(form)

        # Crear la entrada en HistorialPrecio
        HistorialPrecio.objects.create(
            producto=form.instance.producto,
            precio_anterior=form.instance.precio,
            fecha_modificacion=form.instance.fecha_creacion
        )
        return response
    success_url=reverse_lazy('precios_list')
    
def precios_por_productos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    precios_producto = HistorialPrecio.objects.filter(producto=producto)

    # Verificar si la petición es AJAX para devolver JSON
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        precios_data = [
            {
                'id': precio.id,
                'nombre': precio.producto,
                'precio': precio.precio_anterior,
                'fecha': precio.fecha_modificacion,
            }
            for precio in precios_producto
        ]
        return JsonResponse({'precios': precios_data})

    return render(request, 'productos/Precios/precios_historial.html', {
        'producto': producto,
        'precios_producto': precios_producto,
    })


################################SUCURSALES########################################
class SucursalListView (LoginRequiredMixin,ListView):
    model = Sucursal
    template_name="sucursales/sucursal_list.html"
    context_object_name="sucursales"
    login_url='../accounts/login'

class SucursalCreateView(CreateView):
    model=Sucursal
    template_name='sucursales/sucursal_form.html'
    fields=['nombre','ubicacion','descripcion','estado','localidad']
    success_url=reverse_lazy('sucursal_list')

class SucursalDeleteView (DeleteView):
    model=Sucursal
    template_name='sucursales/sucursal_confirm_delete.html'
    success_url=reverse_lazy('sucursal_list')

class SucursalUpdateView (UpdateView):
    model=Sucursal
    template_name='sucursales/sucursal_form.html'
    fields=['nombre','ubicacion','descripcion','estado','localidad']
    success_url=reverse_lazy('sucursal_list')

class SucursalDetailView(DetailView):
    model = Sucursal
    template_name = 'sucursales/sucursal_detail.html'
    context_object_name = 'sucursal'



##################################DEPOSITOS#############################################
class DepositosListView(LoginRequiredMixin,ListView):
    model=Deposito
    template_name = 'depositos/depositos_list.html'
    context_object_name = 'depositos'
    login_url = '../accounts/login/'

class DepositoDetailView(DetailView):
    model = Deposito
    template_name = 'depositos/deposito_detail.html'
    context_object_name = 'deposito'

class DepositoCreateView(CreateView):
    model = Deposito
    template_name = 'depositos/deposito_form.html'

    fields = ['nombre', 'direccion', 'telefono','email','estado','capacidad_maxima','sucursal']

    #fields = '__all__'

    success_url = reverse_lazy('depositos_list')
    

class DepositoUpdateView(UpdateView):
    model = Deposito
    template_name = 'depositos/deposito_form.html'

    fields = '__all__'
    success_url = reverse_lazy('depositos_list')
    def get_context_data(self, **kwargs):
        # Llama al método base para obtener el contexto inicial
        context = super().get_context_data(**kwargs)
        
        # Agrega la lista de objetos del modelo Deposito al contexto
        context['sucursal'] = Sucursal.objects.all()
        return context

class DepositoDeleteView(DeleteView):
    model = Deposito
    template_name = 'depositos/deposito_confirm_delete.html'
    success_url = reverse_lazy('depositos_list')

##################################ORDEN DE COMPRA#############################################

class OrdenCompraView (CreateView):
    model=OrdenCompra
    template_name='compras/compras_orden.html'
    fields =['nordenCompra','fecha','proveedor','fechaentrega','lugarentrega','condiciones']
    success_url=reverse_lazy('orden_list')
    def get_initial(self):
        # Llamar al método original
        initial = super().get_initial()
        # Obtener el último ID de la orden de compra y agregar 1
        ultimo_orden = OrdenCompra.objects.order_by('id').last()
        siguiente_id = (ultimo_orden.id + 1) if ultimo_orden else 1
        # Establecer el valor inicial para 'nordenCompra'
        initial['nordenCompra'] = siguiente_id
        
        return initial
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Asegurar que el campo 'nordenCompra' se establezca como readonly
        form.fields['nordenCompra'].widget.attrs['readonly'] = True
        return form
    
class OrdenCompraListView (LoginRequiredMixin,ListView):
    model = OrdenCompra
    template_name='compras/compras_listaorden.html'
    context_object_name='ordenes'
    login_url='../accounts/login'



class ProveedorListView(LoginRequiredMixin,ListView):
    model=Proveedor
    template_name='proveedores/proveedor_list.html'
    context_object_name='proveedores'
    login_url='../accounts/login'

class ProveedorCreateView(CreateView):
    model=Proveedor
    template_name='proveedores/proveedor_form.html'
    context_object_name='proveedores'
    fields='__all__'
    success_url=reverse_lazy('proveedor_list')

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name='proveedores/proveedor_form.html'
    context_object_name='proveedores'
    fields='__all__'
    success_url=reverse_lazy('proveedor_list')
class ProveedorDeleteView(DeleteView):
    model=Proveedor
    template_name='proveedores/proveedor_delete.html'
    success_url=reverse_lazy('proveedor_list')

class CategoriaListView(LoginRequiredMixin,ListView):
    model=Categoria
    template_name='categorias/categorias_list.html'
    context_object_name='categorias'
    login_url='../accounts/login'

class CategoriaCreateView(CreateView):
    model=Categoria
    template_name='categorias/categorias_form.html'
    context_object_name='categorias'
    fields=['nombre','descripcion']
    success_url=reverse_lazy('categoria_list')

class CategoriaDeleteView (DeleteView):
    model=Categoria
    template_name='categorias/categorias_delete.html'
    success_url=reverse_lazy('categoria_list')

class CategoriaUpdateView (UpdateView):
    model=Categoria
    template_name='categorias/categorias_form.html'
    context_object_name='categorias'
    fields=['nombre','descripcion']
    success_url=reverse_lazy('categoria_list')

##################################ORDEN DE PAGO#############################################

class PagoCreateView (CreateView):
    model = OrdenPago
    template_name='compras/compras_pago.html'
    context_object_name='ordenes'
    fields=['proveedor','nordenPago','fecha','estado','metodo_pago','total']
    success_url=reverse_lazy('pagos_list')
    

def pagos_list(request):
    ordenespago = OrdenPago.objects.all()
    return render (request,'compras/compras_listapago.html',{'ordenes':ordenespago})


def pago_detail(request,pk):
    orden =OrdenPago.objects.get(pk=pk)
    detallesorden = detalleOrdenPago.objects.filter(ordenpago=orden)
    return render (request,'compras/detail_pago.html',{'orden':orden,'detalles':detallesorden})

def get_productos(request):
    proveedor_id = request.GET.get('proveedor_id')
    productos = Producto.objects.filter(proveedor_id=proveedor_id)
    productos_list = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse({'productos': productos_list})


def get_productos_por_deposito(request):
    deposito_id = request.GET.get('deposito_id')
    print(deposito_id)
    productos = ProductoPorDeposito.objects.filter(deposito_id=deposito_id)
    productos_list = [{'id': p.id, 'nombre': p.producto.nombre ,'stock' : p.cantidad} for p in productos]
    return JsonResponse({'productos': productos_list})

def get_productos_por_sucursal(request):
    sucursal_id = request.GET.get('sucursal_id')  # Obtener el ID de la sucursal desde la consulta
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    depositos = sucursal.depositos.all()
    productos_en_sucursal = ProductoPorDeposito.objects.filter(deposito__in=depositos)
    
    productos_list = []
    productos_ids = set()  # Conjunto para rastrear IDs de productos únicos

    for p in productos_en_sucursal:
        # Verificar si el producto ya ha sido añadido
        if p.producto.id not in productos_ids:
            # Obtener el precio actual del producto
            precio_actual = ListaPrecio.objects.filter(producto=p.producto).order_by('-fecha_creacion').first()  # Obtiene el último precio registrado
            precio_unitario = precio_actual.precio if precio_actual else None  # Manejo de si no hay precio
            
            # Añadir producto a la lista y al conjunto
            productos_list.append({
                'id': p.producto.id,
                'nombre': p.producto.nombre,
                'precio_unitario': precio_unitario,
            })
            productos_ids.add(p.producto.id)  # Añadir ID al conjunto para evitar duplicados

    print(productos_list)
    return JsonResponse({'productos': productos_list})
def get_precio(request):
    producto_id = request.GET.get('producto_id')
    producto = Producto.objects.get(id=producto_id)
    print(producto.precio)
    return JsonResponse({'precio_unitario': str(producto.precio)})

def get_facturas(request):
    Proveedor_id=request.GET.get('proveedor_id')
    facturas = FacturasCompras.objects.filter(proveedor=Proveedor_id,estado='Activo')
    facturas_list=[{'id':f.id,'numero':f.numero_factura,'total':f.total} for f in facturas] 
    return JsonResponse({'facturas':list(facturas_list)})

def registrar_pago(request):
    if request.method == "POST":
        try:
            # Parsear los datos enviados en formato JSON
            data = json.loads(request.body)
            print (data)

            # Obtener proveedor
            proveedor = Proveedor.objects.get(nombre=data['proveedor'])

            # Crear la Orden de Pago
            orden_pago = OrdenPago.objects.create(
                proveedor=proveedor,
                nordenPago=data.get('nordenPago', None),
                fecha=data.get('fecha', None),
                metodo_pago=data.get('metodo_pago', None),
                observaciones=data.get('notas', None),
                total=data.get('total', None)
            )


            # Crear los detalles de la orden
            for factura in data['facturas']:
                factura_obj = FacturasCompras.objects.get(numero_factura=factura['numero_factura'])
                detalle_orden = detalleOrdenPago.objects.create(
                    ordenpago=orden_pago,
                    factura=factura_obj,
                    costoenvio=factura.get('costoenvio', 0),
                    subtotal=factura.get('subtotal', 0)

                )
                factura_obj.estado = "Baja"
                factura_obj.save()


            # Retornar una respuesta de éxito
            return JsonResponse({'message': 'Orden de pago registrada exitosamente'})

        except Proveedor.DoesNotExist:
            return JsonResponse({'message': 'Proveedor no encontrado'}, status=400)
        except FacturasCompras.DoesNotExist:
            return JsonResponse({'message': 'Factura no encontrada'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    # Si no es una solicitud POST, retornar un error 405
    return HttpResponse(status=405)

def get_codigo_AFIP(request):
    sucursal_id=request.GET.get('sucursal_id')
    sucursal = Sucursal.objects.get(id=sucursal_id)
    return JsonResponse ({'codigoAFIP':sucursal.codigoAFIP})

def confirmar_orden_compra(request):
    if request.method == 'POST':
        try:
            # Cargar datos del cuerpo de la solicitud
            data = json.loads(request.body)
            
            # Crear una nueva OrdenCompra
            orden_compra = OrdenCompra(
                nordenCompra=data['nordenCompra'],
                proveedor_id=data['proveedor_id'],
                fecha=data['fecha'],
                fechaentrega=data.get('fechaentrega', None),
                lugarentrega_id=data.get('lugarentrega', None),
                condiciones=data.get('condiciones', ''),
                total=data.get("total")
            )
            orden_compra.save()
            
            # Procesar productos
            productos = data.get('productos', [])
            for producto in productos:
                detalle_orden = DetalleOrden(
                    producto_id=producto['productoId'],
                    ordencompra=orden_compra,
                    cantidad=producto['cantidad'],
                    precioUnitario=producto['precioUnitario'],
                    subtotal=producto['subtotal']
                )
                detalle_orden.save()

            return redirect(reverse('orden_list'))
        except KeyError as e:
            # Capturar errores de clave y proporcionar respuesta adecuada
            return JsonResponse({'status': 'error', 'message': f'Falta el campo: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            # Capturar errores en el formato JSON
            return JsonResponse({'status': 'error', 'message': 'Error en el formato JSON'}, status=400)
        except Exception as e:
            # Capturar cualquier otro error
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def get_proveedores(request):
    proveedores = Proveedor.objects.all().values('id', 'nombre')  # Ajusta los campos según tu modelo
    return JsonResponse({'proveedores': list(proveedores)})


def get_depositos(request):
    depositos = Deposito.objects.all().values('id', 'nombre')  # Ajusta los campos según tu modelo
    return JsonResponse({'depositos': list(depositos)})

def get_ordenes(request):
    proveedor_id = request.GET.get('proveedor_id')  # Obtener el ID del proveedor seleccionado
    if proveedor_id:
        # Filtrar las órdenes de compra por el proveedor seleccionado
        ordenes = OrdenCompra.objects.filter(proveedor_id=proveedor_id).filter(estado="Activo").values('id', 'nordenCompra','lugarentrega__sucursal__codigoAFIP')
        return JsonResponse({'ordenes': list(ordenes)})
    return JsonResponse({'ordenes': []})

class ProductoXDepositoListView(LoginRequiredMixin,ListView):
    model = ProductoPorDeposito
    template_name = 'productos_list/producto_list.html'
    context_object_name = 'productos_por_deposito'
    login_url = '../accounts/login/'
    def get_context_data(self, **kwargs):
        # Llama al método base para obtener el contexto inicial
        context = super().get_context_data(**kwargs)
        
        # Agrega la lista de objetos del modelo Deposito al contexto
        context['user'] = self.request.user
        context['depositos'] = Deposito.objects.all()
        context['productos'] = Producto.objects.all()
        return context


class ProductoXDepositoDetailView(DetailView):
    model = ProductoPorDeposito
    template_name = 'productos_list/producto_detail.html'
    context_object_name = 'productos_por_deposito'
    def get_context_data(self, **kwargs):
        # Llama al método base para obtener el contexto inicial
        context = super().get_context_data(**kwargs)
        
        # Agrega la lista de objetos del modelo Deposito al contexto
        context['user'] = self.request.user
        context['depositos'] = Deposito.objects.all()
        context['productos'] = Producto.objects.all()
        return context

class ProductoXDepositoCreateView(CreateView):
    model = ProductoPorDeposito
    template_name = 'productos_list/producto_form.html'
    fields = ['deposito','producto','estado','fecha_ingreso']
    success_url = reverse_lazy('productos_list')
    
    def get_context_data(self, **kwargs):
        # Llama al método base para obtener el contexto inicial
        context = super().get_context_data(**kwargs)
        
        # Agrega la lista de objetos del modelo Deposito al contexto
        context['user'] = self.request.user
        context['depositos'] = Deposito.objects.all()
        context['productos'] = Producto.objects.all()
        return context
    

class ProductoXDepositoUpdateView(UpdateView):
    model = ProductoPorDeposito
    template_name = 'productos_list/producto_form.html'
    fields = ['deposito','producto','estado','fecha_ingreso']
    success_url = reverse_lazy('productos_list')
    

class ProductoXDepositoDeleteView(DeleteView):
    model = ProductoPorDeposito
    template_name = 'productos_list/producto_confirm_delete.html'
    success_url = reverse_lazy('productos_list')


def productos_por_deposito(request, deposito_id):
    deposito = get_object_or_404(Deposito, id=deposito_id)
    productos_en_deposito = ProductoPorDeposito.objects.filter(deposito=deposito)

    # Verificar si la petición es AJAX para devolver JSON
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        productos_data = [
            {
                'id': producto.producto.id,
                'nombre': producto.producto.nombre,
                'precio_unitario': producto.precio_unitario,
                'cantidad_disponible': producto.cantidad_disponible,
            }
            for producto in productos_en_deposito
        ]
        return JsonResponse({'productos': productos_data})

    return render(request, 'productos_list/productos_por_depositos.html', {
        'deposito': deposito,
        'productos_en_deposito': productos_en_deposito,
    })


def productos_por_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    depositos = sucursal.depositos.all()
    productos_en_sucursal = ProductoPorDeposito.objects.filter(deposito__in=depositos)

    # Verificar si la petición es AJAX para devolver JSON
    if request.is_ajax():
        productos_data = [
            {
                'id': producto.producto.id,
                'nombre': producto.producto.nombre,
                'precio_unitario': producto.precio_unitario,
                'cantidad_disponible': producto.cantidad_disponible,
            }
            for producto in productos_en_sucursal
        ]
        return JsonResponse({'productos': productos_data})

    return render(request, 'productos_list/productos_por_sucursal.html', {
        'sucursal': sucursal,
        'productos_en_sucursal': productos_en_sucursal,
    })



def movimientos_list_view(request,deposito_id):
    movimientos = Movement.objects.filter(from_deposito_id = deposito_id)
    deposito = Deposito.objects.get(id=deposito_id)
    return render(request, 'movimientos_list.html',{'movimientos':movimientos,'deposito':deposito})

def movimientos_detail_view(request,movimiento_id):
    movimiento = Movement.objects.get(id=movimiento_id)
    print(movimiento)
    detalles = DetalleMovement.objects.filter(movimiento_id=movimiento.id)
    deposito = Deposito.objects.get(id=movimiento.from_deposito.id)
    print(detalles)
    return render(request,'movimiento_detail.html',{'movimiento':movimiento,'detalles':detalles,'deposito':deposito})


def registrar_movimiento_form(request,deposito_id):
    form = MovimientoForm()
    deposito = get_object_or_404(Deposito, id=deposito_id)
    productos_en_deposito = ProductoPorDeposito.objects.filter(deposito=deposito)
    nro_movimiento = Movement.objects.all().order_by('id').last()
    
    if nro_movimiento:
        nro_movimiento = nro_movimiento.id + 1
    else:
        nro_movimiento = 1
    return render(request, 'registrar_movimiento.html', {
        'deposito': deposito,
        'nro_mov': nro_movimiento,
        'productos': productos_en_deposito,
        'form':form
    })
    


def registrar_movimiento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            
            nroMovimiento = data.get('nroMovimiento')
            referenceDeposito = data.get('referenceDeposito')
            fecha_emision = data.get('fecha_emision')
            estado = data.get('estado')
            tipo_movimiento = data.get('tipo_movimiento')
            motivo = data.get('motivo')
            condiciones = data.get('condiciones')
            productos = data.get('productos')

            # Obtener el deposito
            try:
                deposito_obj = Deposito.objects.get(nombre=referenceDeposito)
                deposito_id = deposito_obj.id
                movimiento = Movement.objects.create(
                nro_movimiento=nroMovimiento, 
                from_deposito=deposito_obj, 
                fecha=fecha_emision, 
                estado=estado,
                tipo_movimiento=tipo_movimiento, 
                motivo=motivo, 
                condiciones=condiciones, 
            )
            except deposito_obj.DoesNotExist:
                return JsonResponse({'message': f'deposito con nombre "{deposito_id}" no encontrado'}, status=400)
            for producto in productos:
                producto_nombre = producto.get('productoNombre', '').strip()
                cantidad = producto.get('cantidad')

                # Validar campos de producto
                if not producto_nombre or not cantidad:
                    print('Datos de producto inválidos:', producto)  # Agregar impresión para depuración
                    continue  # O puedes retornar un error si prefieres

                try:
                    producto_obj = Producto.objects.get(nombre=producto_nombre)
                    producto_deposito = ProductoPorDeposito.objects.filter(producto=producto_obj,deposito=deposito_obj)
                    if producto_deposito.exists():
                        # Obtén el objeto individual
                        producto = producto_deposito.first()  # o usa .get() si estás seguro de que solo hay uno

                        if tipo_movimiento == 'ING':
                            # Incrementar la cantidad actual
                            producto.cantidad += int(cantidad)
                        else:
                            # Calcular la nueva cantidad asegurando que no sea negativa
                            nueva_cantidad = producto.cantidad - int(cantidad)
                            if nueva_cantidad < 0:
                                raise ValueError("La cantidad no puede ser negativa.")
                            producto.cantidad = nueva_cantidad

                        # Guarda los cambios en la base de datos
                        producto.save()
                    else:
                        print("No se encontró el producto en el depósito.")
                    DetalleMovement.objects.create(
                        movimiento=movimiento,
                        producto=producto_obj,
                        cantidad=cantidad
                    )
                except Producto.DoesNotExist:
                    return JsonResponse({'message': f'Producto "{producto_nombre}" no encontrado'}, status=400)  
                
            return JsonResponse({'message': 'Movimiento registrado exitosamente'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

def exito(request):
    return render(request, 'exito.html')

def detalleorden(request,pk):
    orden = OrdenCompra.objects.get(pk=pk)
    detalles = DetalleOrden.objects.filter(ordencompra=orden)
    return render (request,'compras/detail_orden.html',{'orden':orden,'detalles':detalles})

def get_orden_detalles(request):
    orden_id = request.GET.get('orden_id')
    
    # Si 'orden_id' no está presente, retorna un error o un mensaje adecuado
    if not orden_id:
        return JsonResponse({'error': 'orden_id no proporcionado'}, status=400)
    
    # Obtén la orden con 'get' en lugar de 'filter' para un único resultado
    try:
        orden = OrdenCompra.objects.get(id=orden_id)
    except OrdenCompra.DoesNotExist:
        return JsonResponse({'error': 'Orden no encontrada'}, status=404)

    # Filtra los detalles usando el objeto 'orden'
    detalles = DetalleOrden.objects.filter(ordencompra=orden)
    detalles_data = [{
        'producto_nombre': detalle.producto.nombre,
        'cantidad': detalle.cantidad,
        'precio':detalle.precioUnitario,
        'subtotal':detalle.subtotal
    } for detalle in detalles]

    return JsonResponse({'detallesOrden': detalles_data})


def Facturas_list(request):
    facturas = FacturasCompras.objects.all()
    return render (request,'compras/compras_factura.html',{'facturas':facturas})


def detalleFactura(request,pk):
    factura = FacturasCompras.objects.get(pk=pk)
    detalles = DetalleFactura.objects.filter(factura=factura)
    return render (request,'compras/detail_factura.html',{'factura':factura,'detalles':detalles})

class createFactura(CreateView):
    model = FacturasCompras
    template_name = 'compras/registrar_factura.html'
    fields = ['reference_orden','proveedor','numero_factura','tipo_factura','fecha_emision','descuento','impuestos','estado','notas','total']
    success_url = reverse_lazy('facturas_list')
    


def getDetalleOrden(request):
    orden_id = request.GET.get('orden_id')
    try:
        detalle_orden = DetalleOrden.objects.filter(ordencompra_id=orden_id)
        productos = [{'id': d.producto.id, 'nombre': d.producto.nombre, 'cantidad': d.cantidad} for d in detalle_orden]
        return JsonResponse({'productos': productos})
    except OrdenCompra.DoesNotExist:
        return JsonResponse({'error': 'Orden no encontrada'}, status=404)

def registrar_factura(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            referencia_orden = data.get('reference_orden')
            tipo_factura = data.get('tipo_factura')
            proveedor_id = data.get('proveedor_id')
            numero_factura = data.get('numero_factura')
            fecha_emision = data.get('fecha_emision')
            codigo_factura=data.get('codigo_factura')
            notas = data.get('notas')

            total = data.get('total')
            productos = data.get('productos')

            # Obtener y actualizar la orden de compra
            try:
                orden = OrdenCompra.objects.get(id=referencia_orden)
                orden.estado = 'Baja'
                orden.save()
            except OrdenCompra.DoesNotExist:
                return JsonResponse({'message': f'Orden de compra con ID "{referencia_orden}" no encontrada'}, status=400)

            # Obtener el proveedor
            try:
                proveedor_obj = Proveedor.objects.get(nombre=proveedor_id)
                proveedor_id = proveedor_obj.id
            except Proveedor.DoesNotExist:
                return JsonResponse({'message': f'Proveedor con nombre "{proveedor_id}" no encontrado'}, status=400)

            # Crear la factura
            factura = FacturasCompras.objects.create(
                reference_orden=orden,
                proveedor_id=proveedor_id,
                tipo_factura=tipo_factura,
                numero_factura=numero_factura,
                fecha_emision=fecha_emision,
                notas=notas,
                total=total,
                codigo_factura=codigo_factura
            )

            # Procesar los productos
            for producto in productos:
                producto_nombre = producto.get('productoNombre', '').strip()
                cantidad = producto.get('cantidad')
                precio = producto.get('precio')
                subtotal = producto.get('subtotal')

                # Validar campos de producto
                if not producto_nombre or not cantidad or not precio or not subtotal:
                    print('Datos de producto inválidos:', producto)  # Agregar impresión para depuración
                    continue  # O puedes retornar un error si prefieres

                try:
                    producto_obj = Producto.objects.get(nombre=producto_nombre)
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto_obj,
                        cantidad=cantidad,
                        preciounitario=precio,
                        subtotal=subtotal
                    )
                except Producto.DoesNotExist:
                    return JsonResponse({'message': f'Producto "{producto_nombre}" no encontrado'}, status=400)

            return JsonResponse({'message': 'Factura registrada exitosamente'})

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Error al procesar los datos JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)


def EcommerceHome (request):
    sucursales = Sucursal.objects.all()
    coordenadas = obtener_latitud_longitud(4400, 'AR')
    if coordenadas:
        print(f"Latitud: {coordenadas['latitud']}, Longitud: {coordenadas['longitud']}")
    else:
        print("No se encontraron coordenadas para el código postal proporcionado.") 
    if request.user.groups.filter(name='admin').exists():
        productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad')).filter(total_stock__gt=0)
        categorias = Categoria.objects.all()
        client_group = Group.objects.get(name='client')
        clientes = User.objects.filter(groups=client_group)
        consultas = Consulta.objects.all()
        return render(request, 'ecommerce/admin_main.html',{'productos':productos,'categorias':categorias,'clientes':clientes,'consultas':consultas})
    elif request.user.groups.filter(name='client').exists():
        return render (request,'ecommerce/main.html',{'sucursales':sucursales})
    else:
        return render (request,'ecommerce/main.html',{'sucursales':sucursales})


    

def ListProducts (request):
    cat = request.GET.get('category')
    latest_price = ListaPrecio.objects.filter(producto=OuterRef('pk')).order_by('-fecha_creacion').values('precio')[:1]
    if cat :
        category = Categoria.objects.get(nombre=cat)
        productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad'), precio_actual=Subquery(latest_price)).filter(total_stock__gt=0, categoria=category)
        categorias = Categoria.objects.all()
        return render (request, 'ecommerce/productos.html',{'productos': productos,'categorias':categorias,'cat':category})

    else:
        productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad'), precio_actual=Subquery(latest_price)).filter(total_stock__gt=0)
        categorias = Categoria.objects.all()
        return render (request, 'ecommerce/productos.html',{'productos': productos,'categorias':categorias})

def LoginView (request):
    return render (request, 'ecommerce/login.html')

def ContactView (request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Su consulta fue enviada satisfactoriamente.'})
        else:
            return JsonResponse({'success': False, 'message': 'Hubo un error al enviar la consulta. Por favor, intente de nuevo.'})
    else:
        form = ConsultaForm()
    
    return render(request, 'ecommerce/contact.html', {'form': form})

def EcommerceLoginView(request):

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        form_register = CustomUserCreationForm(request.POST)
        if 'register' in request.POST and form_register.is_valid():
            user = form_register.save()
            client_group = Group.objects.get(name='client')
            client_group.user_set.add(user)
            login(request, user)  # Loguear automáticamente al usuario después de registrarse
            messages.success(request, f"Cuenta creada con éxito para {user.username}")
            return redirect('tienda')  # Redirigir a la página principal o donde desees
        else:
            messages.error(request, "Error al crear la cuenta. Verifica los datos.")

        if 'login_form' in request.POST and form.is_valid():
            print('login')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tienda')  # Redirige a la página principal o donde quieras
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Error en la validación del formulario')
    else:
        form = CustomLoginForm()

    return render(request, 'ecommerce/login.html', {'form': form})

@csrf_exempt
def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect('/tienda')

def mi_cuenta(request):
    username = request.user
    user = User.objects.get(username=username)
    return render(request,'ecommerce/mi_cuenta.html',{'user':user})

def get_products_json(request):
    # Obtener todos los productos (puedes añadir filtros si lo deseas)
    productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad')).filter(total_stock__gt=0)

    # Crear una lista de productos en formato JSON
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'stock':producto.total_stock
        })
    # Devolver la respuesta en JSON
    return JsonResponse({'productos': productos_list})

@csrf_exempt
def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect('/tienda')

def checkout(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        form_register = CustomUserCreationForm(request.POST)
        if 'register' in request.POST and form_register.is_valid():
            user = form_register.save()
            client_group = Group.objects.get(name='client')
            client_group.user_set.add(user)
            login(request, user)  # Loguear automáticamente al usuario después de registrarse
            messages.success(request, f"Cuenta creada con éxito para {user.username}")
            return redirect('checkout')  # Redirigir a la página principal o donde desees
        else:
            messages.error(request, "Error al crear la cuenta. Verifica los datos.")

        if 'login_form' in request.POST and form.is_valid():
            print('login')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('checkout')  # Redirige a la página principal o donde quieras
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Error en la validación del formulario')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            # Obtén los datos del JSON
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            address = data.get('address')
            city = data.get('city')
            postalCode = data.get('postalCode')
            titular = data.get('titular')
            dniTitular = data.get('dniTitular')
            cardNumber = data.get('cardNumber')
            expiry = data.get('expiry')
            cvv = data.get('cvv')
            products = data.get('products')  # Lista de productos [{nombre, cantidad, precio}, ...]

            user = User.objects.get(username=request.user)

            # Lista de campos obligatorios
            required_fields = [
                name, email, phone, address, city, postalCode,
                titular, dniTitular, cardNumber, expiry, cvv, products
            ]

            # Verifica si alguno de los campos obligatorios es None o vacío
            if any(field is None or field == '' for field in required_fields):
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios.'}, status=400)

            # Crear la orden de venta
            orden = OrdenVentaOnline.objects.create(
                nro_orden='ORD-{}'.format(OrdenVentaOnline.objects.count() + 1),  # Genera un número de orden único
                status='Pendiente',  # Puedes cambiar el estado según tu lógica
                fecha=datetime.now(),
                user=user,
                nombre_completo=name,
                correo_electronico=email,
                telefono=phone,
                direccion=address,
                cuidad=city,
                codigo_postal=postalCode,
                titular_tarjeta=titular,
                dni_tarjeta=dniTitular,
                numero_tarjeta=cardNumber,
                exp_tarjeta=expiry,
                cvv_tarjeta=cvv,
            )


            ultimate_factura = FacturaVenta.objects.order_by('-id').first()
            sucursal = Sucursal.objects.first()
            tienda_online = Cliente.objects.get(id=1)
            factura = FacturaVenta.objects.create(
            numeroFactura=ultimate_factura.id+8,  # Use the order number as the invoice number, or generate a new one
            fecha=datetime.now(),  # Make sure to set the correct deposito
            metodo_pago='Tarjeta',  # Set according to your logic
            total=0,  # Initialize total, you can calculate it after adding details
            observaciones='',  # Set any relevant observations
            descuento=0,
            sucursal=sucursal,
            cliente = tienda_online 
            )

            # Crear detalles de venta para cada producto
            total_price = 0
            for product in products:
                producto_id = product.get('id')  # Debes asegurarte de que el nombre corresponda a un objeto Producto en tu base de datos
                cantidad = product.get('quantity')
                precio = product.get('price')

                # Obtener la instancia del producto y su stock
                try:
                    producto_instance = Producto.objects.get(id=producto_id)

                    # Buscar el stock del producto en el depósito correspondiente (suponiendo que se maneja el stock por depósito)
                    stock_item = ProductoPorDeposito.objects.filter(producto=producto_instance).first()

                    if stock_item and stock_item.cantidad >= cantidad:
                        # Descontar el stock
                        stock_item.cantidad -= cantidad
                        stock_item.save()

                        # Crear el detalle de la venta
                        DetalleVentaOnline.objects.create(
                            producto=producto_instance,
                            OrdenVentaOnline=orden,
                            cantidad=cantidad,
                            precio=precio,
                            subtotal=cantidad * precio,  # Calcula el subtotal
                        )
                        total_price += cantidad * precio  # Accumulate total price for invoice
                        DetalleVenta.objects.create(
                            producto=producto_instance,
                            facturaventa=factura,  # Link the detail to the created invoice
                            cantidad=cantidad,
                            precio=precio,
                            subtotal=cantidad * precio,
                        )
                        # Update the invoice total
                    else:
                        return JsonResponse({'success': False, 'message': f'Stock insuficiente para el producto {producto_instance.nombreProducto}'}, status=400)
                except Producto.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'El producto {producto_id} no existe.'}, status=400)

            factura.total = total_price
            factura.save()
            return JsonResponse({'success': True, 'message': 'Su pedido fue procesado con éxito', 'cod': orden.nro_orden})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    else:
        if request.user.is_authenticated:
            return render(request, 'ecommerce/checkout.html')
        else:
            return render(request, 'ecommerce/login.html')


###################### Clientes #####################
class ClientesListaView(LoginRequiredMixin,ListView):
    model = Cliente
    template_name="ventas/ListaClientes.html"
    context_object_name='clientes'
    login_url='../accounts/login/'

def guardar_cliente(request):
    if request.method=='POST':
        cuit = request.POST.get('cuit')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        if not all ([cuit,nombre,apellido,email,telefono]):
            return JsonResponse({'status':'error','message':'Por favor, complete todos los campos del formulario'})
        try:
            cliente = Cliente(cuit=cuit,nombre=nombre,apellido=apellido,email=email,telefono=telefono)
            cliente.save()
            return JsonResponse({'status':'success','message':'Cliente guardado exitosamente'})
        except Exception as e:
            return JsonResponse({'status':'error','message':'Ocurrio un error al guardar el cliente'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


###################### Ventas #####################

class VentasListView (LoginRequiredMixin,ListView):
    model = FacturaVenta
    template_name='ventas/ListaVentas.html'
    context_object_name='ventas'
    login_url='../accounts/login/'

class VentasCreateView (CreateView):
    model= FacturaVenta
    template_name='ventas/registrar_Venta.html'
    fields='__all__'
    success_url='ventas_list'
    def get_initial(self):
        # Llamar al método original
        initial = super().get_initial()
        # Obtener el último ID de la orden de compra y agregar 1
        ultimo_orden = FacturaVenta.objects.order_by('id').last()
        siguiente_id = (ultimo_orden.id + 1) if ultimo_orden else 1
        # Establecer el valor inicial para 'nordenCompra'
        initial['numeroFactura'] = siguiente_id
        
        return initial
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Asegurar que el campo 'nordenCompra' se establezca como readonly
        form.fields['numeroFactura'].widget.attrs['readonly'] = True
        return form

def ventas_detalle(request,pk):
    facturaventa =FacturaVenta.objects.get(pk=pk)
    detallesventa = DetalleVenta.objects.filter(facturaventa=facturaventa)
    return render (request,'ventas/ventas_detail.html',{'ventas':facturaventa,'detalles':detallesventa})

def guardar_venta (request):
    if request.method=="POST":
        data = json.loads(request.body)

        numero_factura = data.get('numero_factura')
        fecha = data.get('fecha')
        sucursal_id = data.get('sucursal')
        cliente_id = data.get('cliente')
        metodo_pago = data.get('metodo_pago')
        observaciones = data.get('condiciones', '')
        total=data.get('total')
        codigo_sucursal=data.get('codigo_sucursal')

        cliente=Cliente.objects.get(id=cliente_id)
        sucursal=Sucursal.objects.get(id=sucursal_id)

        factura = FacturaVenta.objects.create(
            numeroFactura=numero_factura,
            fecha=fecha,
            sucursal=sucursal,
            cliente=cliente,
            metodo_pago=metodo_pago,
            observaciones=observaciones,
            total=total,
            codigo_sucursal=codigo_sucursal
        )
        for producto_data in data['productos']:
            producto_nombre = producto_data['productoNombre']
            cantidad = producto_data['cantidad']
            precio = producto_data['precio']
            subtotal = producto_data['subtotal']
            producto = Producto.objects.get(nombre=producto_nombre)
            DetalleVenta.objects.create(
                producto=producto,
                facturaventa=factura,
                cantidad=cantidad,
                precio=precio,
                subtotal=subtotal
            )
        return JsonResponse({'status': 'success', 'message': 'Venta guardada exitosamente'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

#### INFORMES #####


def generar_informe(request):
    tipo = request.GET.get('tipo')
    hoy = datetime.today().date()

    # Filtrar órdenes según el tipo de informe
    if tipo == 'diario':
        ordenes = OrdenCompra.objects.filter(fecha=hoy)
    elif tipo == 'semanal':
        semana_pasada = hoy - timedelta(days=7)
        ordenes = OrdenCompra.objects.filter(fecha__range=[semana_pasada, hoy])
    elif tipo == 'mensual':
        mes_pasado = hoy - timedelta(days=30)
        ordenes = OrdenCompra.objects.filter(fecha__range=[mes_pasado, hoy])

    # Crear el buffer de memoria para el PDF
    buffer = io.BytesIO()

    # Crear el lienzo de ReportLab en el buffer
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    # Insertar la imagen del logo en la esquina superior izquierda
    logo_url = "https://i.ibb.co/T0PqHb5/logo-bluedragon.jpg"
    p.drawImage(logo_url, 50, height - 100, width=90, height=90)  # Ajusta el tamaño y posición según necesites

    # Configurar el título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Informe de Órdenes de Compra {tipo.upper()} ")
    p.setFont("Helvetica-Bold", 13)
    p.drawString(200, height - 80, f"Fecha: {hoy}")

    # Crear la tabla de órdenes con proveedor y cantidad total de productos
    data = [["N° Orden", "Fecha", "Estado", "Proveedor", "Cantidad Total de Productos"]]

    # Crear diccionario para almacenar la cantidad de productos por proveedor
    productos_por_proveedor = {}
    estado_ordenes = {"Activo": 0, "Baja": 0}  # Inicializar diccionario para los estados

    for orden in ordenes:
        # Calcular la cantidad total de productos de la orden
        detalles = DetalleOrden.objects.filter(ordencompra=orden)
        total_productos = sum([detalle.cantidad for detalle in detalles])

        # Obtener el proveedor asociado a la orden
        proveedor = orden.proveedor.nombre

        # Contabilizar la cantidad de órdenes por estado
        if orden.estado in estado_ordenes:
            estado_ordenes[orden.estado] += 1
        else:
            estado_ordenes[orden.estado] = 1

        # Agregar la cantidad de productos por proveedor
        if proveedor in productos_por_proveedor:
            productos_por_proveedor[proveedor] += total_productos
        else:
            productos_por_proveedor[proveedor] = total_productos

        # Agregar datos a la tabla
        data.append([orden.nordenCompra, orden.fecha.strftime('%d-%m-%Y'), orden.estado, proveedor, total_productos])

    # Crear la tabla usando ReportLab
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Calcular la altura de la tabla para ajustar la posición de los gráficos
    table_width, table_height = table.wrap(width - 100, height)  # Calcula el tamaño de la tabla

    # Dibujar la tabla en el PDF
    table.drawOn(p, 50, height - 125 - table_height)  # Ajustar la posición en función de la altura de la tabla

    # Crear el primer gráfico de productos por proveedor
    fig, ax = plt.subplots(figsize=(6, 3))
    proveedores = list(productos_por_proveedor.keys())
    cantidades = list(productos_por_proveedor.values())
    ax.barh(proveedores, cantidades, color='skyblue')
    ax.set_xlabel('Cantidad de Productos')
    ax.set_title('Cantidad de Productos por Proveedor')
    plt.tight_layout()

    # Guardar el primer gráfico en un buffer de memoria
    graph_buffer = io.BytesIO()
    plt.savefig(graph_buffer, format='png')
    plt.close(fig)
    graph_buffer.seek(0)

    # Insertar el primer gráfico en el PDF debajo de la tabla
    imagen = ImageReader(graph_buffer)
    p.drawImage(imagen, 50, height - 200 - table_height - 150, width=420, height=200)

    # Crear el segundo gráfico de estados de las órdenes
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    estados = list(estado_ordenes.keys())
    cantidades_estados = list(estado_ordenes.values())
    ax2.bar(estados, cantidades_estados, color=['green', 'red'])  # Colores distintos para cada estado
    ax2.set_xlabel('Estado')
    ax2.set_ylabel('Cantidad de Órdenes')
    ax2.set_title('Cantidad de Órdenes por Estado')
    plt.tight_layout()

    # Guardar el segundo gráfico en un nuevo buffer de memoria
    graph_buffer2 = io.BytesIO()
    plt.savefig(graph_buffer2, format='png')
    plt.close(fig2)
    graph_buffer2.seek(0)

    # Insertar el segundo gráfico en el PDF debajo del primer gráfico
    imagen2 = ImageReader(graph_buffer2)
    p.drawImage(imagen2, 50, height - 200 - table_height - 400, width=420, height=200)

    # Cerrar el lienzo y terminar el PDF
    p.showPage()
    p.save()

    # Movemos el contenido del buffer al principio
    buffer.seek(0)

    # Creamos la respuesta HTTP con el contenido del PDF generado
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{tipo}_{datetime.today()}.pdf"'

    return response

def generar_informe_ventas(request):
    tipo = request.GET.get('tipo')
    hoy = datetime.today().date()

    # Filtrar facturas según el tipo de informe
    if tipo == 'diario':
        facturas = FacturaVenta.objects.filter(fecha=hoy)
    elif tipo == 'semanal':
        semana_pasada = hoy - timedelta(days=7)
        facturas = FacturaVenta.objects.filter(fecha__range=[semana_pasada, hoy])
    elif tipo == 'mensual':
        mes_pasado = hoy - timedelta(days=30)
        facturas = FacturaVenta.objects.filter(fecha__range=[mes_pasado, hoy])

    # Calcular ingresos totales
    ingresos_totales = sum([factura.total for factura in facturas])

    # Crear el buffer de memoria para el PDF
    buffer = io.BytesIO()

    # Crear el lienzo de ReportLab en el buffer
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Insertar la imagen del logo en la esquina superior izquierda
    logo_url = "https://i.ibb.co/T0PqHb5/logo-bluedragon.jpg"
    p.drawImage(logo_url, 50, height - 100, width=90, height=90)

    # Configurar el título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Informe de Ventas {tipo.upper()}")
    p.setFont("Helvetica-Bold", 13)
    p.drawString(200, height - 80, f"Fecha: {hoy}")

    # Crear la tabla con los datos de las ventas
    data = [["N° F", "N° Detalle", "Producto", "Cantidad", "Subtotal", "Método de Pago"]]

    # Diccionarios para los gráficos
    productos_subtotal = {}
    facturas_metodopago = {}

    for factura in facturas:
        detalles = DetalleVenta.objects.filter(facturaventa=factura)
        for detalle in detalles:
            producto_nombre = detalle.producto.nombre
            subtotal = detalle.subtotal

            # Agregar datos de la factura a la tabla
            data.append([
                factura.numeroFactura,
                detalle.id,  # Número de detalle factura
                producto_nombre,
                detalle.cantidad,
                subtotal,
                factura.metodo_pago
            ])

            # Sumar el subtotal de productos
            if producto_nombre in productos_subtotal:
                productos_subtotal[producto_nombre] += subtotal
            else:
                productos_subtotal[producto_nombre] = subtotal

        # Contabilizar facturas por método de pago
        if factura.metodo_pago in facturas_metodopago:
            facturas_metodopago[factura.metodo_pago] += factura.total
        else:
            facturas_metodopago[factura.metodo_pago] = factura.total

    # Agregar la fila de "Ingresos Totales" al final de la tabla
    data.append(["", "", "", "Ingresos Totales", ingresos_totales, ""])

    # Crear la tabla usando ReportLab
    col_widths = [40, 50, 150, 80, 80, 110]  # Ajusta estos valores según lo necesites
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Color especial para la fila de Ingresos Totales
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),  # Alineación vertical
        ('WORDWRAP', (0, 1), (-1, -1), 'TRUE')
    ]))

    # Calcular la altura de la tabla para ajustar la posición de los gráficos
    table_width, table_height = table.wrap(width - 100, height)

    # Dibujar la tabla en el PDF
    table.drawOn(p, 50, height - 125 - table_height)

    # Crear el primer gráfico: Productos x Subtotal
    fig, ax = plt.subplots(figsize=(6, 3))
    productos = list(productos_subtotal.keys())
    subtotales = list(productos_subtotal.values())
    ax.barh(productos, subtotales, color='skyblue')
    ax.set_xlabel('Subtotal')
    ax.set_title('Subtotal por Producto')
    plt.tight_layout()

    # Guardar el primer gráfico en un buffer de memoria
    graph_buffer = io.BytesIO()
    plt.savefig(graph_buffer, format='png')
    plt.close(fig)
    graph_buffer.seek(0)

    # Insertar el primer gráfico en el PDF
    imagen = ImageReader(graph_buffer)
    p.drawImage(imagen, 50, height - 200 - table_height - 150, width=420, height=200)

    # Crear el segundo gráfico: Facturas x Método de Pago
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    metodos_pago = list(facturas_metodopago.keys())
    totales_metodopago = list(facturas_metodopago.values())
    ax2.pie(totales_metodopago, labels=metodos_pago, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
    ax2.set_title('Total de Ventas por Método de Pago')
    plt.tight_layout()

    # Guardar el segundo gráfico en un nuevo buffer de memoria
    graph_buffer2 = io.BytesIO()
    plt.savefig(graph_buffer2, format='png')
    plt.close(fig2)
    graph_buffer2.seek(0)

    # Insertar el segundo gráfico en el PDF
    imagen2 = ImageReader(graph_buffer2)
    p.drawImage(imagen2, 50, height - 200 - table_height - 400, width=420, height=200)

    # Cerrar el lienzo y finalizar el PDF
    p.showPage()
    p.save()

    # Movemos el contenido del buffer al principio
    buffer.seek(0)

    # Crear la respuesta HTTP con el contenido del PDF generado
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_ventas_{tipo}_{datetime.today()}.pdf"'

    return response

def generar_informe_facturas(request):
    tipo = request.GET.get('tipo')
    hoy = datetime.today().date()

    # Filtrar facturas según el tipo de informe
    if tipo == 'diario':
        facturas = FacturasCompras.objects.filter(fecha_emision=hoy)
    elif tipo == 'semanal':
        semana_pasada = hoy - timedelta(days=7)
        facturas = FacturasCompras.objects.filter(fecha_emision__range=[semana_pasada, hoy])
    elif tipo == 'mensual':
        mes_pasado = hoy - timedelta(days=30)
        facturas = FacturasCompras.objects.filter(fecha_emision__range=[mes_pasado, hoy])

    # Calcular egresos totales
    egresos_totales = sum([factura.total for factura in facturas])

    # Crear el buffer de memoria para el PDF
    buffer = io.BytesIO()

    # Crear el lienzo de ReportLab en el buffer
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Insertar la imagen del logo en la esquina superior izquierda
    logo_url = "https://i.ibb.co/T0PqHb5/logo-bluedragon.jpg"
    p.drawImage(logo_url, 50, height - 100, width=90, height=90)

    # Configurar el título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Informe de Compras {tipo.upper()}")
    p.setFont("Helvetica-Bold", 13)
    p.drawString(200, height - 80, f"Fecha: {hoy}")

    # Crear la tabla con los datos de las facturas
    data = [["N°Factura", "N°Detalle", "Producto", "Cantidad", "Subtotal", "Tipo Factura"]]

    # Diccionarios para los gráficos
    productos_subtotal = {}
    proveedores_facturas = {}
    tipos_factura_count = {}
    facturas_procesadas = set()  # Conjunto para rastrear facturas ya contadas

    for factura in facturas:
        detalles = DetalleFactura.objects.filter(factura=factura)
        for detalle in detalles:
            producto_nombre = detalle.producto.nombre
            subtotal = detalle.subtotal

        # Agregar datos de la factura a la tabla
            data.append([
                factura.numero_factura,
                detalle.id,  # Número de detalle factura
                producto_nombre,
                detalle.cantidad,
                subtotal,
                factura.tipo_factura,
            ])

        # Sumar el subtotal de productos
            if producto_nombre in productos_subtotal:
                productos_subtotal[producto_nombre] += subtotal
            else:
                productos_subtotal[producto_nombre] = subtotal

        # Contabilizar facturas por proveedor
            if factura.proveedor.nombre in proveedores_facturas:
                proveedores_facturas[factura.proveedor.nombre] += factura.total
            else:
                proveedores_facturas[factura.proveedor.nombre] = factura.total

            # Contabilizar facturas por tipo solo si no se ha contado antes
            if factura.id not in facturas_procesadas:
                if factura.tipo_factura in tipos_factura_count:
                    tipos_factura_count[factura.tipo_factura] += 1
                else:
                    tipos_factura_count[factura.tipo_factura] = 1
                facturas_procesadas.add(factura.id) 

    # Agregar la fila de "Egresos Totales" al final de la tabla
    data.append(["", "", "", "Egresos Totales", egresos_totales, ""])

    # Crear la tabla usando ReportLab
    col_widths = [60, 60, 150, 80, 80, 100, 100]  # Ajusta estos valores según lo necesites
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Color especial para la fila de Egresos Totales
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),  # Alineación vertical
        ('WORDWRAP', (0, 1), (-1, -1), 'TRUE')
    ]))

    # Calcular la altura de la tabla para ajustar la posición de los gráficos
    table_width, table_height = table.wrap(width - 100, height)

    # Dibujar la tabla en el PDF
    table.drawOn(p, 50, height - 125 - table_height)

    # Crear el primer gráfico: Productos x Subtotal
    plt.figure(figsize=(6, 3))
    productos = list(productos_subtotal.keys())
    subtotales = list(productos_subtotal.values())
    plt.barh(productos, subtotales, color='skyblue')
    plt.xlabel('Subtotal')
    plt.title('Subtotal por Producto')
    
    # Guardar el gráfico en un buffer
    plt.tight_layout()
    plt.savefig('producto_subtotal.png', format='png')
    plt.close()

    # Insertar el primer gráfico en el PDF
    p.drawImage('producto_subtotal.png', 50, height - 200 - table_height - 100, width=420, height=150)

    # Crear el segundo gráfico: Proveedores x Facturas
    plt.figure(figsize=(6, 3))
    proveedores = list(proveedores_facturas.keys())
    totales_proveedores = list(proveedores_facturas.values())
    plt.barh(proveedores, totales_proveedores, color='lightgreen')
    plt.xlabel('Total de Facturas')
    plt.title('Total de Compras por Proveedor')
    
    # Guardar el gráfico en un buffer
    plt.tight_layout()
    plt.savefig('proveedores_facturas.png', format='png')
    plt.close()

    # Insertar el segundo gráfico en el PDF
    p.drawImage('proveedores_facturas.png', 50, height - 150 - table_height - 300, width=420, height=150)

    # Crear el tercer gráfico: Facturas x Tipo de Factura
    plt.figure(figsize=(6, 3))
    tipos_factura = list(tipos_factura_count.keys())
    cantidades = list(tipos_factura_count.values())
    plt.bar(tipos_factura, cantidades, color='salmon')
    plt.ylabel('Cantidad de Facturas')
    plt.title('Cantidad de Facturas por Tipo')
    
    # Guardar el gráfico en un buffer
    plt.tight_layout()
    plt.savefig('tipos_factura.png', format='png')
    plt.close()

    # Insertar el tercer gráfico en el PDF
    p.drawImage('tipos_factura.png', 50, height - 150 - table_height - 450, width=420, height=150)

    # Cerrar el lienzo y finalizar el PDF
    p.showPage()
    p.save()

    # Movemos el contenido del buffer al principio
    buffer.seek(0)

    # Crear la respuesta HTTP con el contenido del PDF generado
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_compras_{tipo}_{datetime.today()}.pdf"'

    return response

def admin_productos(request):
    productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad')).filter(total_stock__gt=0)

    return render(request,'ecommerce/productos_list.html',{'productos':productos})
def admin_producto_edit(request,pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    context = {
        'producto': producto
    }
    return render(request,'ecommerce/prod_detail.html',context)
def agregar_imagenes(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if request.method == 'POST' and request.FILES:
        for file in request.FILES.getlist('imageFile'):
            # Crear una nueva instancia de Media para cada archivo subido
            media = Media(content=file, mimetype=file.content_type, name=file.name)
            media.save()
            producto.media.add(media)  # Asocia la imagen al producto
        return redirect('admin_prods_edit', pk=producto.id)
    return render(request, 'agregar_imagenes.html', {'producto': producto})

def eliminar_imagen(request, producto_id, media_id):
    producto = get_object_or_404(Producto, id=producto_id)
    media = get_object_or_404(Media, id=media_id)

    # Elimina la imagen del producto
    producto.media.remove(media)
    media.delete()  # Si deseas eliminar el archivo de la base de datos también

    return redirect('admin_prods_edit', pk=producto.id)  # Redirige a la vista del producto
def mis_ordenes(request):
    user = User.objects.get(username=request.user)
    ordenes = OrdenVentaOnline.objects.filter(user=user).order_by('-id')
    print(ordenes)
    return render(request,'ecommerce/mis_ordenes.html',{'ordenes': ordenes})

def detalle_orden(request, orden_id):
    # Obtén la orden por ID
    orden = get_object_or_404(OrdenVentaOnline, id=orden_id, user=request.user)
    # Obtén los detalles de la orden
    detalles = DetalleVentaOnline.objects.filter(OrdenVentaOnline=orden)

    context = {
        'orden': orden,
        'detalles': detalles,
    }
    
    return render(request, 'ecommerce/detalle_orden.html', context)
def nosotros(request):
    return render(request,'ecommerce/nosotros.html')
def admin_consultas(request):
    consultas = Consulta.objects.all().order_by('estado')
    
    return render(request,'ecommerce/admin_consultas.html',{'consultas':consultas})


def responder_consultas(request):
    if request.method == 'POST':
        try:
            # Cargar el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
            mensaje = data.get('mensaje')
            consulta_id = data.get('consulta')
            print(data)

            # Obtener la consulta correspondiente
            consulta = get_object_or_404(Consulta, id=int(consulta_id))

            # Guardar la respuesta en el campo 'respuesta' del modelo
            consulta.respuesta = mensaje
            consulta.estado = 'respondida'  # Cambiar el estado si es necesario
            consulta.save()

            # Devolver una respuesta exitosa
            return JsonResponse({'success': True, 'message': 'Respuesta enviada correctamente.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error al procesar los datos.'}, status=500)

    # En caso de que el método no sea POST
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=500)

def ingresos_egresos_view(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Asegúrate de que las fechas sean válidas
    if not fecha_inicio or not fecha_fin:
        return JsonResponse({'error': 'Fechas inválidas'}, status=400)

    # Obtener los ingresos con fecha truncada
    ingresos = list(FacturaVenta.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin]
    ).annotate(
        fecha_trunc=Cast(F('fecha'), output_field=models.DateField())  # Trunca la fecha
    ).values('fecha_trunc')
    .annotate(total=Sum('total'))
    .order_by('fecha_trunc'))

    egresos = list(FacturasCompras.objects.filter(
        fecha_emision__range=[fecha_inicio, fecha_fin]
    ).annotate(
        fecha_trunc=Cast(F('fecha_emision'), output_field=models.DateField())  # Trunca la fecha
    ).values('fecha_trunc')
    .annotate(total=Sum('total'))
    .order_by('fecha_trunc'))

    # Generar un rango de fechas
    start_date = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    end_date = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    fecha_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Crear una lista de ingresos acumulativos
    ingresos_acumulados = []
    total_ingresos = 0
    for fecha in fecha_range:
        total_diario = next((item['total'] for item in ingresos if item['fecha_trunc'] == fecha), 0)
        total_ingresos += total_diario
        ingresos_acumulados.append({'fecha_trunc': fecha, 'total': total_ingresos})

    # Crear una lista de egresos acumulativos
    egresos_acumulados = []
    total_egresos = 0
    for fecha in fecha_range:
        total_diario = next((item['total'] for item in egresos if item['fecha_trunc'] == fecha), 0)
        total_egresos += total_diario
        egresos_acumulados.append({'fecha_trunc': fecha, 'total': total_egresos})

    return JsonResponse({
        'ingresos': ingresos_acumulados,
        'egresos': egresos_acumulados,
    })
def marca_mas_vendida(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Primero filtras las ventas en el rango de fechas
    ventas_en_periodo = FacturaVenta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Luego buscas los detalles de las ventas filtradas
    marcas = DetalleVenta.objects.filter(facturaventa__in=ventas_en_periodo)\
        .values('producto__proveedor__nombre')\
        .annotate(cantidad_total=Sum('cantidad'))\
        .order_by('-cantidad_total')[:3]

    return JsonResponse(list(marcas), safe=False)

def categoria_mas_vendida(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Primero filtras las ventas en el rango de fechas
    ventas_en_periodo = FacturaVenta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        # Calcular la categoría más vendida
    categorias = DetalleVenta.objects.filter(facturaventa__in=ventas_en_periodo).values('producto__categoria__nombre') \
            .annotate(cantidad_total=Sum('cantidad')) \
            .order_by('-cantidad_total')
    return JsonResponse(list(categorias), safe=False)

def empleado_mas_vendio(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

        # Calcular el empleado que más vendió
    sucursales = FacturaVenta.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).values('sucursal__nombre') \
            .annotate(ventas_totales=Sum('total')) \
            .order_by('-ventas_totales')
    print (sucursales)
    return JsonResponse(list(sucursales), safe=False)


def ventas_online(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')    
        # Calcular las ventas online por estado
    ventas_online = OrdenVentaOnline.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).values('status') \
            .annotate(cantidad_total=Count('status')) \
            .order_by('-cantidad_total')

    return JsonResponse(list(ventas_online), safe=False)

def productos_mas_vendidos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    ventas_en_periodo = FacturaVenta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

    productos_vendidos = (
        DetalleVenta.objects.filter(facturaventa__in =ventas_en_periodo)
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')[:5]
    )
    print(productos_vendidos)
    return JsonResponse(list(productos_vendidos), safe=False)

def listar_ventas(request):
    ventas = OrdenVentaOnline.objects.all().order_by('-id')
    return render(request, 'ecommerce/ventas.html', {'ventas': ventas})
def listar_ventas_entregadas(request):
    ventas = OrdenVentaOnline.objects.filter(status='entregado').order_by('-id')
    return render(request, 'ecommerce/ventas_entregadas.html', {'ventas': ventas})

def cambiar_estado(request, orden_id):
    if request.method == 'POST':
        orden = OrdenVentaOnline.objects.get(id=orden_id)
        data = json.loads(request.body)
        nuevo_estado = data.get('estado')

        if nuevo_estado in ['preparacion', 'despachado', 'entregado']:
            orden.status = nuevo_estado
            orden.save()
            return JsonResponse({'success': True, 'message': 'Estado actualizado'})
        else:
            return JsonResponse({'success': False, 'message': 'Estado no válido'}, status=400)
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


def listar_ventas_pendientes(request):
    ventas = OrdenVentaOnline.objects.filter(status='Pendiente').order_by('-id')
    return render(request, 'ecommerce/ventas_pendientes.html', {'ventas': ventas})
def listar_ventas_despachadas(request):
    ventas = OrdenVentaOnline.objects.filter(status='despachado').order_by('-id')
    return render(request, 'ecommerce/ventas_despachadas.html', {'ventas': ventas})
def listar_ventas_preparacion(request):
    ventas = OrdenVentaOnline.objects.filter(status='preparacion').order_by('-id')
    return render(request, 'ecommerce/ventas_preparacion.html', {'ventas': ventas})