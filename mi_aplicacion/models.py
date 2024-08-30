
# Create your models here.
from django.db import models

class Provincia(models.Model):
    nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    estado = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Sucursal (models.Model):
    nombre=models.CharField(max_length=255)
    ubicacion=models.CharField(max_length=255)
    descripcion=models.TextField(blank=True,null=True)
    localidad = models.ForeignKey(Localidad,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.nombre

    def __str__(self):
        return self.nombre


class Deposito(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    capacidad_maxima = models.IntegerField(blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal,on_delete=models.SET_NULL,null=True,blank=True,related_name='depositos')
    def __str__(self):
        return self.nombre
    


class Proveedor (models.Model):
    cuit = models.CharField(max_length=20,unique=True,default='0')
    nombre = models.CharField(max_length=100)  # Nombre del proveedor
    domicilio = models.CharField(max_length=255, null=True, blank=True)  # Dirección del proveedor
    telefono = models.CharField(max_length=20, null=True, blank=True)  # Teléfono de contacto
    correo = models.EmailField(null=True, blank=True)  # Correo electrónico de contacto
    sitio_web = models.URLField(null=True, blank=True)  # Sitio web del proveedor
    status = models.BooleanField(default=True)  # Estado del proveedor (activo/inactivo)
    fecha_registro = models.DateTimeField(null=True,blank=True)  # Fecha de registro del proveedor
    descripcion = models.TextField(null=True, blank=True)  # Descripción del proveedor
    categoria = models.CharField(max_length=50, null=True, blank=True)  # Categoría del proveedor

    def __str__(self):
        return self.nombre
class Categoria (models.Model):
    nombre=models.CharField(max_length=255,blank=True,null=True)
    descripcion=models.TextField(blank=True,null=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ProductoPorDeposito(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)  
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
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
    total = models.DecimalField(max_digits=15,decimal_places=2,blank=True,null=True)
    def __str__(self):
        return f"Orden N°: 000000{self.nordenCompra} | Proveedor: {self.proveedor}"

class DetalleOrden (models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    ordecompra=models.ForeignKey(OrdenCompra,on_delete=models.CASCADE)
    precio_unitario=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    cantidad=models.IntegerField(blank=True,null=True)
    subtotal=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)


class FacturasCompras (models.Model):
    reference_orden = models.ForeignKey(OrdenCompra,on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True,default='0000000000')
    tipo_factura = models.CharField(max_length=20,choices=[('A','A'),('B','B'),('C','C')])
    fecha_emision = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2 , default=0.21)
    estado = models.CharField(max_length=20, choices=[('Pagada', 'Pagada'), ('Pendiente', 'Pendiente'), ('Cancelada', 'Cancelada')])
    metodo_pago = models.CharField(max_length=50,choices=[('Efectivo', 'Efectivo'), ('Credito', 'Credito'), ('Debito', 'Debito')])
    detalles = models.TextField(null=True, blank=True)
    vendedor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    notas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.proveedor.nombre}"




class Movement(models.Model):
    from_branch = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='movements_out')
    to_branch = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='movements_in')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movement from {self.from_branch} to {self.to_branch} on {self.date}"

class MovementProduct(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name='movement_products')
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.movement}"

