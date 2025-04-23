# Proceso de instalación 

## Antes de hacer un commit, agrega el codigo de instalación en caso de que hayas hecho algun pip install o otra instalacion!!


1. Crea tu entorno virtual
- python -m venv venv
  
2. Activa tu entorno virtual
- venv\Scripts\activate

3. Instalar Django en el entorno virutal
- pip install django

4. Instalar Bootstrap
- pip install django-bootstrap-v5

5. Crea un nuevo proyecto de Django (no hacer)
- django-admin startproject ferremaxProject

6. creamos la app
- python manage.py startapp myFerremax


# Codigo de migracion y inicio del proeycto

- venv\Scripts\activate 

- cd ferremaxProject        

sirve para crear archivos de migración que reflejan los cambios que has hecho en los modelos (models.py) de tu aplicación.

- python manage.py makemigrations

- python manage.py migrate  

- python manage.py runserver