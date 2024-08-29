
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
    

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    
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