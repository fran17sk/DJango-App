
# Create your models here.
from django.db import models

class Provincia(models.Model):
    nombre = models.CharField(max_length=255,blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=255,blank=True, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')

    def __str__(self):
        return f'{self.nombre} - {self.provincia}' 

class Sucursal (models.Model):
    nombre=models.CharField(max_length=255,blank=True, null=True)
    ubicacion=models.CharField(max_length=255,blank=True, null=True)
    descripcion=models.TextField(blank=True,null=True)
    localidad = models.ForeignKey(Localidad,on_delete=models.SET_NULL,null=True,blank=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')

    def __str__(self):
        return self.nombre

class Deposito(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255,blank=True, null=True)
    direccion = models.CharField(max_length=255,blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')
    capacidad_maxima = models.IntegerField(blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal,on_delete=models.SET_NULL,null=True,blank=True,related_name='depositos')
    def __str__(self):
        return self.nombre
    
class Proveedor (models.Model):
    cuit = models.CharField(max_length=20,unique=True,default='0')
    nombre = models.CharField(max_length=100)  
    domicilio = models.CharField(max_length=255, null=True, blank=True)  
    telefono = models.CharField(max_length=20, null=True, blank=True)  
    correo = models.EmailField(null=True, blank=True)  
    sitio_web = models.URLField(null=True, blank=True)  
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')
    fecha_registro = models.DateTimeField(null=True,blank=True)  
    descripcion = models.TextField(null=True, blank=True)  
    categoria = models.CharField(max_length=50, null=True, blank=True)  

    def __str__(self):
        return self.nombre
    
class Categoria (models.Model):
    nombre=models.CharField(max_length=255,blank=True,null=True)
    descripcion=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255,blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ProductoPorDeposito(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0,blank=True, null=True)  
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')
    stock_actual = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre} en {self.deposito.nombre}"

class OrdenCompra (models.Model):
    nordenCompra = models.IntegerField(blank=True,null=True)
    fecha = models.DateField(blank=True,null=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    fechaentrega=models.DateField(blank=True,null=True)
    lugarentrega=models.ForeignKey(Deposito,on_delete=models.CASCADE,null=True)
    condiciones = models.TextField(blank=True,null=True)
    estado = models.TextField(blank=True,default="Activo")
    def __str__(self):
        return f"Orden N°: {self.nordenCompra}"

class DetalleOrden (models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    ordencompra=models.ForeignKey(OrdenCompra,on_delete=models.CASCADE)
    cantidad=models.IntegerField(blank=True,null=True)

class FacturasCompras (models.Model):
    reference_orden = models.ForeignKey(OrdenCompra,on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True,default='0000000000',blank=True, null=True)
    tipo_factura = models.CharField(max_length=20,blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2 , default=0.21,blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='Activo')
    vendedor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    notas = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)


    def __str__(self):
        return f"Factura {self.numero_factura} - {self.proveedor.nombre}"


class DetalleFactura (models.Model):
    factura = models.ForeignKey(FacturasCompras,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=3,decimal_places=0,null=True,blank=True)
    preciounitario=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    subtotal=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

class OrdenPago (models.Model):
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    nordenPago = models.CharField(max_length=20,unique=True,blank=True,null=True)
    fecha = models.DateField(blank=True,null=True)
    estado = models.CharField(max_length=20,default='activo')
    metodo_pago=models.CharField(max_length=20,blank=True,null=True)
    observaciones=models.TextField(blank=True,null=True)
    total = models.DecimalField(max_digits=15,decimal_places=2,blank=True,null=True)

class detalleOrdenPago(models.Model):
    ordenpago = models.ForeignKey(OrdenPago,on_delete=models.CASCADE)
    factura = models.ForeignKey(FacturasCompras,on_delete=models.CASCADE)
    costoenvio = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

class Movement(models.Model):
    nMov = models.IntegerField(blank=True,null=True)
    from_deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE, related_name='movements_out')
    date = models.DateTimeField(blank=True, null=True)
    fecha = models.DateField(blank=True,null=True)
    condiciones = models.TextField(blank=True,null=True)
    def __str__(self):
        return f"Movement from {self.from_deposito} on {self.date}"

class DetalleMovement(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name='movement_product')
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, null=True)    

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.movement}"