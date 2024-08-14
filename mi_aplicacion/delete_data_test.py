from mi_aplicacion.models import Provincia, Localidad, Deposito, Producto, ProductoPorDeposito

def run():
    # Eliminar productos por depósitos
    ProductoPorDeposito.objects.all().delete()

    # Eliminar productos
    Producto.objects.all().delete()

    # Eliminar depósitos
    Deposito.objects.all().delete()

    # Eliminar localidades
    Localidad.objects.all().delete()

    # Eliminar provincias
    Provincia.objects.all().delete()