from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto,Sucursal
from .models import Producto,ProductoPorDeposito,Deposito,OrdenCompra,Proveedor,DetalleOrden
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def home(request):
    return render(request, 'base.html')
class ProductoListView(LoginRequiredMixin,ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'
    login_url = '../accounts/login/'
    def get_context_data(self, **kwargs):
        # Llama al método base para obtener el contexto inicial
        context = super().get_context_data(**kwargs)
        
        # Agrega la lista de objetos del modelo Deposito al contexto
        context['user'] = self.request.user
        context['depositos'] = Deposito.objects.all()
        context['productos_por_deposito'] = ProductoPorDeposito.objects.all()
        return context
 

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio','categoria','estado','proveedor']
    success_url = reverse_lazy('producto_list')
    

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio','categoria','estado']
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

class SucursalListView (LoginRequiredMixin,ListView):
    model = Sucursal
    template_name="sucursales/sucursal_list.html"
    context_object_name="sucursal"
    login_url='../accounts/login'

class SucursalCreateView(CreateView):
    model=Sucursal
    template_name='sucursales/sucursal_form.html'
    fields=['nombre','ubicacion','descripcion']
    success_url=reverse_lazy('sucursal_list')

class SucursalDeleteView (DeleteView):
    model=Sucursal
    template_name='sucursales/sucursal_confirm_delete.html'
    success_url=reverse_lazy('sucursal_list')

class SucursalUpdateView (UpdateView):
    model=Sucursal
    template_name='sucursales/sucursal_form.html'
    fields=['nombre','ubicacion','descripcion']
    success_url=reverse_lazy('sucursal_list')
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
    success_url = reverse_lazy('depositos_list')
    

class DepositoUpdateView(UpdateView):
    model = Deposito
    template_name = 'depositos/deposito_form.html'
    fields = ['nombre', 'direccion', 'telefono','email','estado','capacidad_maxima','sucursal']
    success_url = reverse_lazy('depositos_list')

class DepositoDeleteView(DeleteView):
    model = Deposito
    template_name = 'depositos/deposito_confirm_delete.html'
    success_url = reverse_lazy('depositos_list')

class OrdenCompraView (CreateView):
    model=OrdenCompra
    template_name='compras/compras_orden.html'
    fields =['nordenCompra','fecha','proveedor','fechaentrega','lugarentrega','condiciones','total']

class ProveedorListView(LoginRequiredMixin,ListView):
    model=Proveedor
    template_name='proveedores/proveedor_list.html'
    context_object_name='proveedores'
    login_url='../accounts/login'
class ProveedorCreateView(CreateView):
    model=Proveedor
    template_name='proveedores/proveedor_form.html'
    context_object_name='proveedores'
    fields=['nombre','correo','domicilio']
    success_url=reverse_lazy('proveedor_list')
class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name='proveedores/proveedor_form.html'
    context_object_name='proveedores'
    fields=['nombre','correo','domicilio']
    success_url=reverse_lazy('proveedor_list')
class ProveedorDeleteView(DeleteView):
    model=Proveedor
    template_name='proveedores/proveedor_delete.html'
    success_url=reverse_lazy('proveedor_list')

from django.http import JsonResponse
from .models import Producto

def get_productos(request):
    proveedor_id = request.GET.get('proveedor_id')
    productos = Producto.objects.filter(proveedor_id=proveedor_id)
    productos_list = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse({'productos': productos_list})

def get_precio(request):
    producto_id = request.GET.get('producto_id')
    producto = Producto.objects.get(id=producto_id)
    return JsonResponse({'precio_unitario': str(producto.precio_unitario)})


def confirmar_orden_compra(request):
    if request.method == 'POST':
        try:
            # Cargar datos del cuerpo de la solicitud
            data = json.loads(request.body)
            
            # Crear una nueva OrdenCompra
            orden_compra = OrdenCompra(
                proveedor_id=data['proveedor_id'],
                fecha=data['fecha'],
                fechaentrega=data.get('fechaentrega', None),
                lugarentrega_id=data.get('lugarentrega', None),
                condiciones=data.get('condiciones', ''),
                total=0  # Este valor se actualizará después
            )
            orden_compra.save()
            
            # Procesar productos
            productos = data.get('productos', [])
            total_orden = 0
            for producto in productos:
                detalle_orden = DetalleOrden(
                    producto_id=producto['productoId'],
                    ordecompra=orden_compra,
                    precio_unitario=producto['precioUnitario'],
                    cantidad=producto['cantidad'],
                    subtotal=producto['subtotal']
                )
                detalle_orden.save()
                total_orden += float(producto['subtotal'])
            
            # Actualizar el total en OrdenCompra
            orden_compra.total = total_orden
            orden_compra.save()

            return JsonResponse({'status': 'success'})
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