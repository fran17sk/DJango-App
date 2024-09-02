from mi_aplicacion.models import *

def run():
    ProductoPorDeposito.objects.all().delete()
    Producto.objects.all().delete()
    Deposito.objects.all().delete()
    Localidad.objects.all().delete()
    Provincia.objects.all().delete()
    Sucursal.objects.all().delete()
    Proveedor.objects.all().delete()
    Categoria.objects.all().delete()
    OrdenCompra.objects.all().delete()
    DetalleOrden.objects.all().delete()
    FacturasCompras.objects.all().delete()
    Movement.objects.all().delete()
    DetalleMovement.objects.all().delete()