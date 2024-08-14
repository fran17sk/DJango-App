from mi_aplicacion.models import Provincia, Localidad, Deposito, Producto, ProductoPorDeposito

def run():
    # Crear provincias
    provincias = []
    for i in range(1, 11):
        provincia = Provincia.objects.create(nombre=f"Provincia {i}", estado="Activo")
        provincias.append(provincia)

    # Crear localidades
    localidades = []
    for i in range(1, 11):
        localidad = Localidad.objects.create(nombre=f"Localidad {i}", provincia=provincias[i % len(provincias)], estado="Activo")
        localidades.append(localidad)

    # Crear depósitos
    depositos = []
    for i in range(1, 11):
        deposito = Deposito.objects.create(
            nombre=f"Deposito {i}",
            direccion=f"Direccion {i}",
            telefono=f"12345678{i}",
            email=f"deposito{i}@example.com",
            estado="Activo",
            capacidad_maxima=1000 + i * 100,
            localidad=localidades[i % len(localidades)]
        )
        depositos.append(deposito)

    # Crear productos
    productos = []
    for i in range(1, 11):
        producto = Producto.objects.create(
            nombre=f"Producto {i}",
            descripcion=f"Descripcion del producto {i}",
            precio=10.50 + i,
            categoria="Hardware",
            estado="Activo"
        )
        productos.append(producto)

    # Crear productos por depósitos
    for i in range(1, 11):
        ProductoPorDeposito.objects.create(
            deposito=depositos[i % len(depositos)],
            producto=productos[i % len(productos)],
            cantidad=100 + i * 10,
            fecha_ingreso=f"2023-01-{i:02d}",
            estado="Disponible",
            stock_actual=100 + i * 10
        )