# Carta a la orden

> Se debe tener previamente intalado [**Python**](https://www.python.org/downloads/) igual o por encima de la versión 3.11.1 y [**PostgreSQL**](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) igual o por encima de la versión 15.2.

## Instalar Django

```
pip install django
```

## Instalar complementos de Django

> Se usara **django-filter** para la creación de los filtros de búsqueda, **Pillow** para el manejo de imagenes en la base de datos y **psycopg2** para las actualizaciones de las tablas en la base de datos.

```
pip install django-filter
pip install Pillow
pip install psycopg2
```

## Ingresar la base de datos

> Buscar el archivo **settings.py** en la carpeta de **Carta_a_la_orden**, e ir a la linea donde se encuentre lo siguiente:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'NOMBRE_DE_LA_BASE_DE_DATOS',
        'USER': 'NOMBRE_DEL_USUARIO_DE_LA_BASE_DE_DATOS',
        'PASSWORD': 'CONTRASEÑA_DE_LA_BASE_DE_DATOS',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
> Modificar los campos de **NAME**, **USER** y **PASSWORD** por los datos pertinentes.

## Ejecutar servidor

### Para Windows

```python
py .\manage.py runserver
```

### Para Linux

```python
python .\manage.py runserver
```