from django.http import JsonResponse
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
    ordenes = OrdenCompra.objects.filter(estado="Activo").select_related('proveedor').values('id','nordenCompra','proveedor__nombre')
    return JsonResponse({'ordenes':list(ordenes)})


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
            except deposito_obj.DoesNotExist:
                return JsonResponse({'message': f'deposito con nombre "{deposito_id}" no encontrado'}, status=400)
            deposito = Deposito.objects.get(nombre=referenceDeposito)
            movimiento = Movement.objects.create(
                nro_movimiento=nroMovimiento, 
                from_deposito=deposito, 
                fecha=fecha_emision, 
                estado=estado,
                tipo_movimiento=tipo_movimiento, 
                motivo=motivo, 
                condiciones=condiciones, 
            )
            for producto in productos:
                producto_nombre = producto.get('productoNombre', '').strip()
                cantidad = producto.get('cantidad')

                # Validar campos de producto
                if not producto_nombre or not cantidad:
                    print('Datos de producto inválidos:', producto)  # Agregar impresión para depuración
                    continue  # O puedes retornar un error si prefieres

                try:
                    producto_obj = Producto.objects.get(nombre=producto_nombre)
                    producto_deposito = ProductoPorDeposito.objects.filter(producto=producto_obj)
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
            tipofactura=data.get('tipo_factura')
            notas = data.get('notas')
            impuestos = data.get('impuestos')
            descuento = data.get('descuento')
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
                impuestos=impuestos,
                descuento=descuento,
                total=total
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
