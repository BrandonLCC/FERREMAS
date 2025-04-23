# Proceso de instalación 

## Antes de hacer un commit, agrega el codigo de instalación en caso de que hayas hecho algun pip install o otra instalacion!!

1. Crea tu entorno virtual
``` python -m venv venv ```
  
2. Activa tu entorno virtual
``` venv\Scripts\activate ```

3. Instalar Django en el entorno virutal
``` pip install django ```

4. Instalar Bootstrap
``` pip install django-bootstrap-v5 ```

5. creamos la app
``` python manage.py startapp myFerremax ```


# Codigo de migracion y inicio del proyecto

``` venv\Scripts\activate ```

- Acceder a la carpeta
``` cd ferremaxProject ```   

sirve para crear archivos de migración que reflejan los cambios que has hecho en los modelos (models.py) de tu aplicación.

``` python manage.py makemigrations ```

``` python manage.py migrate  ```

``` python manage.py runserver ```

# Ignorar entorno virtual para los commits
**1. Antes de que subas un commit, asegúrate de que no estás subiendo el entorno virtual al repositorio.**
- Ingresa almenos este codigo al archivo ubicado en el entorno virtual .gitignore
- Entorno virtual - (si le diste otro nombre a tu entorno virtual debes cambiarle el nombre)


Codigo del archivo .gitignore

```
venv/
env/
ENV/
.venv/
.env/
```

