# DJango-App
Para clonar el repositorio
Primero deben tener instalado git en su computadora. 
En una carpeta de tu directorio local abre el cmd, y ejecuta el siguinte comando
`git clone url`

Para levantar la app primero deben instalar django 

`pip install django`

Una vez instalado debes instalar las demas dependecias segun sea tu caso.
`pip install`

Para levantar el servicio debes posicionarte en la carpeta ./DjangoPrueba

Abrir el cmd y ejecutar 
`python manage.py runserver 0.0.0.0:8000`
Esto lanzara la aplicacion que la podras visualizar en la ip 127.0.0.1:8000/


Para evitar errores en la rama principal porfavor crear sus propias ramas
Ejemplo: `git branch user_dev`
luego posicionarse en ella: `git overflow user_dev`
Y recien hacer cambios en el codigo


Si desean visualizar la base de datos de sql lite, debes instalar una extencion de sqlite la primera que te sale al buscar sqlite