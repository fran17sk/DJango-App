
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

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
    
class Media (models.Model):
    content  = models.FileField(upload_to='media/')
    mimetype = models.CharField(max_length=100)
    name     = models.CharField(max_length=255)
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255,blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    media = models.ManyToManyField(Media, blank=True)


    def __str__(self):
        return self.nombre

class ProductoPorDeposito(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0,blank=True, null=True)  
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20,choices=[('activo','activo'),('baja','baja')],default='activo')

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

    TIPO_MOVIMIENTO_CHOICES = [
        ('ING', 'Ingreso'),
        ('EGR', 'Egreso'),
    ]

    MOTIVOS_INGRESO_CHOICES = [
        ('COMPRA', 'Compra de Productos'),
        ('DEV_CLIENTE', 'Devoluciones de Clientes'),
        ('TRANS_INT', 'Transferencias Internas'),
        ('PROD_INT', 'Producción Interna'),
        ('CORR_INV', 'Corrección de Inventario'),
        ('PROMO', 'Promociones o Muestras Gratis'),
        ('REPARACION', 'Retornos por Reparación'),
    ]

    MOTIVOS_EGRESO_CHOICES = [
        ('VENTA', 'Venta a Clientes'),
        ('DEV_PROV', 'Devoluciones a Proveedores'),
        ('TRANS_INT', 'Transferencias Internas'),
        ('MERMA', 'Mermas o Desperdicio'),
        ('PRESTAMO', 'Préstamos'),
        ('CONSIGN', 'Consignaciones'),
        ('DEMO', 'Muestras para Demostración'),
        ('CORR_INV', 'Corrección de Inventario'),
    ]

    tipo_movimiento = models.CharField(
        max_length=3,
        choices=TIPO_MOVIMIENTO_CHOICES,
        default='ING',
    )

    motivo = models.CharField(
        max_length=20,
        choices=MOTIVOS_INGRESO_CHOICES + MOTIVOS_EGRESO_CHOICES,
    )
    nro_movimiento =models.CharField(max_length=20,blank=True,null=True)
    from_deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE, related_name='movements_out')
    fecha = models.CharField(max_length=20,blank=True,null=True)
    estado = models.CharField(max_length=20,blank=True,null=True)
    condiciones = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.get_tipo_movimiento_display()} - {self.get_motivo_display()}'

    def save(self, *args, **kwargs):
        if self.tipo_movimiento == 'ING' and self.motivo not in dict(self.MOTIVOS_INGRESO_CHOICES):
            raise ValueError("El motivo no es válido para un ingreso.")
        elif self.tipo_movimiento == 'EGR' and self.motivo not in dict(self.MOTIVOS_EGRESO_CHOICES):
            raise ValueError("El motivo no es válido para un egreso.")
        super().save(*args, **kwargs)
    

class DetalleMovement(models.Model):
    movimiento = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name='movement_product')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(blank=True, null=True)    

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} in {self.movimiento}"

class Consulta(models.Model):
    nombre = models.CharField(max_length=255,blank=True,null=True)
    correo = models.CharField(max_length=255,blank=True,null=True)
    telefono = models.CharField(max_length=255,blank=True,null=True)
    consulta = models.CharField(max_length=255,blank=True,null=True)
    estado = models.CharField(max_length=20,choices=[('recived','recived'),('respondido','respondido')],default='recived',blank=True,null=True)
    fecha = models.DateField(blank=True,null=True,auto_now_add=True)
    respuesta = models.TextField(blank=True, null=True)
    fecha_respuesta = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.correo}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True,null=True)
    telefono = models.CharField(max_length=20, blank=True,null=True)
    mail = models.CharField(max_length=100, blank=True,null=True)
    localidad = models.CharField(max_length=255, blank=True,null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

class OrdenVentaOnline (models.Model):
    nro_orden = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    fecha = models.DateField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    correo_electronico = models.EmailField()
    telefono = models.PositiveIntegerField(blank=True,null=True)
    direccion = models.CharField(max_length=255)
    cuidad = models.CharField(max_length=255)
    codigo_postal = models.PositiveBigIntegerField() 
    titular_tarjeta = models.CharField(max_length=255)
    dni_tarjeta = models.PositiveBigIntegerField()
    numero_tarjeta = models.PositiveBigIntegerField()
    exp_tarjeta = models.CharField(max_length=255)
    cvv_tarjeta = models.PositiveBigIntegerField()

    def get_status_color(self):
            if self.status == "pendiente":
                return "red"
            elif self.status == "entregado":
                return "green"
            elif self.status == "despachado":
                return "blue"
            elif self.status == "cancelado":
                return "red"
            return "black"  # Por defecto si no coincide
class DetalleVentaOnline (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    OrdenVentaOnline = models.ForeignKey(OrdenVentaOnline, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(blank=False, null=False)
    precio = models.FloatField(blank=False, null=False)
    subtotal = models.FloatField(blank=False, null=False)