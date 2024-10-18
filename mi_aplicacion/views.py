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
from django.db.models import Sum
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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


def  productos_por_deposito(request,deposito_id):
    deposito = get_object_or_404(Deposito, id=deposito_id)
    productos_en_deposito = ProductoPorDeposito.objects.filter(deposito=deposito)

    return render(request, 'productos_list/productos_por_depositos.html', {
        'deposito': deposito,
        'productos_en_deposito': productos_en_deposito,
    })


def productos_por_sucursal(request,sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    depositos = sucursal.depositos.all()
    productos_en_sucursal = ProductoPorDeposito.objects.filter(deposito__in=depositos)

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


def EcommerceHome (request):
    sucursales = Sucursal.objects.all()
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
    if cat :
        category = Categoria.objects.get(nombre=cat)
        productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad')).filter(total_stock__gt=0, categoria=category)
        categorias = Categoria.objects.all()
        return render (request, 'ecommerce/productos.html',{'productos': productos,'categorias':categorias,'cat':category})

    else:
        productos = Producto.objects.annotate(total_stock = Sum('productopordeposito__cantidad')).filter(total_stock__gt=0)
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
    productos = Producto.objects.all()

    # Crear una lista de productos en formato JSON
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto.id,
            'nombre': producto.nombre,
        })
    # Devolver la respuesta en JSON
    return JsonResponse({'productos': productos_list})

@csrf_exempt
def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect('/tienda')


@login_required
def checkout(request):
    return render (request, 'ecommerce/checkout.html')

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