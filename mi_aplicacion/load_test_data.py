from mi_aplicacion.models import Provincia, Localidad, Sucursal
provincia = Provincia(nombre="Salta", estado="Activo")
provincia.save()
localidad = Localidad(nombre="Salta Capital" , provincia=provincia, estado="Activo")
localidad.save()
sucursal = Sucursal(nombre="Sucursal Norte", ubicacion="Dirección Ejemplo", descripcion="Descripción Ejemplo", localidad=localidad)
sucursal.save()