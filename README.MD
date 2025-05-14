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

5. Instalar pilow si lo requiere
``` python -m pip install Pillow    ```

6. Instalar jazzmin para el adminstador
``` pip install -U django-jazzmin   ```

7. Instalar djangorestframework
``` pip install djangorestframework ``` 

8. Instalar transbank-sdk para el uso de WebPay

``` pip install transbank-sdk   ```

# Codigo de migracion y inicio del proyecto

- Activa el entorno si no esta activado
``` venv\Scripts\activate ```

- Acceder a la carpeta
``` cd ferremaxProject ```   

makemigrations: sirve para crear archivos de migración que reflejan los cambios que has hecho en los modelos (models.py) de tu aplicación.

``` python manage.py makemigrations ```

``` python manage.py migrate  ```

``` python manage.py runserver ```

# Ignorar entorno virtual para los commits
**1. Antes de que subas un commit, asegúrate de que no estás subiendo el entorno virtual al repositorio.**
- Ingresa al menos este codigo al archivo ubicado en el entorno virtual .gitignore
- Entorno virtual - (si le diste otro nombre a tu entorno virtual debes cambiarle el nombre)


Codigo del archivo .gitignore

```
venv/
env/
ENV/
.venv/
.env/
```

## Proceso de integración de WebPay  (actualizado 14-05)

- RECORDATORIO: Instalación del SDK 

``` pip install transbank-sdk   ```

1. Creación del template iniciar_pago.html y resultado_pago.html (para proxima entrega, realizar pago fallido y crear un template en donde vuelva a realizar el pago)
2. Creacion de la views Iniciar_pago y Resultado_pago para redireccionar a la pagina una vez realizado el pago  
3. Creacion de la urls 
4. (Por realizar): Se requiere Crear el modelo de compras para almacenar los registros de los usuarios
