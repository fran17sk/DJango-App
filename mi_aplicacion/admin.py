from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Producto)
admin.site.register(Deposito)
admin.site.register(Sucursal)
admin.site.register(ProductoPorDeposito)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(OrdenCompra)
admin.site.register(Proveedor)
admin.site.register(FacturasCompras)
admin.site.register(Categoria)


