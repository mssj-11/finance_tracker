#   Proceso de construcción del proyecto


###	Crear el entorno virtual
```sh
virtualenv venv
```

####	Activar el entorno virtual
```sh
venv\Scripts\activate
```

####	Desactivar el entorno virtual
```sh
deactivate
```

###	Instalar dependencias manualemnte
```sh
pip install django sqlalchemy pandas matplotlib plotly xhtml2pdf
```
Puedes optar esta version tambien:
```sh
pip install django pandas plotly xhtml2pdf
```
####	Registrar las dependencias instaladas
```sh
pip freeze > requirements.txt
```

###	Crear el proyecto Django
```sh
django-admin startproject finance_tracker .
```

###	Correr proyecto
```sh
python manage.py runserver
```

Verificar en la URL: `http://127.0.0.1:8000/`


###	Crea una aplicación para gestionar los gastos, presupuestos y reportes:
```sh
python manage.py startapp expenses
```

####    Configurar los archivos

Modelo de base de datos: `expenses/models.py`
Rutas (URLs): Dentro de las carpetas `finance_tracker` & `expenses` el archivo `urls.py`
Modelos: `models.py`


####	Crea carpetas adicionales: 
Ingresar a `expenses` y ejecutar el comando para crear las carpetas `templates` & `static`:
```sh
mkdir templates static
```


###	Configurar el proyecto: 
Agrega la aplicación `expenses` al archivo `settings.py` en `INSTALLED_APPS`:
```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expenses',  # Nuestra nueva app
]
```




#   Creacion de migraciones:
Crear las migraciones a partir de la definicion del modelo y aplicarlas a expenses
```sh
python manage.py makemigrations expenses
python manage.py migrate
```





