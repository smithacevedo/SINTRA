```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app configuration
   |    |-- settings.py                    # Defines Global Settings
   |    |-- wsgi.py                        # Start the app in production
   |    |-- urls.py                        # Define URLs served by all apps/nodes
   |
   |-- apps/
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- views.py                  # Serve HTML pages for authenticated users
   |    |    |-- urls.py                   # Define some super simple routes  
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- urls.py                   # Define authentication routes  
   |    |    |-- views.py                  # Handles login and registration  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |         |-- includes/                 # HTML chunks and components
   |         |    |-- navigation.html      # Top menu component
   |         |    |-- sidebar.html         # Sidebar component
   |         |    |-- footer.html          # App Footer
   |         |    |-- scripts.html         # Scripts common to all pages
   |         |
   |         |-- layouts/                   # Master pages
   |         |    |-- base-fullscreen.html  # Used by Authentication pages
   |         |    |-- base.html             # Used by common pages
   |         |
   |         |-- accounts/                  # Authentication pages
   |         |    |-- login.html            # Login page
   |         |    |-- register.html         # Register page
   |         |
   |         |-- home/                      # UI Kit Pages
   |              |-- index.html            # Index page
   |              |-- 404-page.html         # 404 page
   |              |-- *.html                # All other pages
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- manage.py                            # Start the app - Django default start script
   |
   |-- ************************************************************************
```



## Licensing

- Copyright 2019 - present [Creative Tim](https://www.creative-tim.com/)
- Licensed under [Creative Tim EULA](https://www.creative-tim.com/license)


---
[Material Dashboard Django](https://www.creative-tim.com/product/material-dashboard-django) - Provided by [Creative Tim](https://www.creative-tim.com/) and [AppSeed](https://appseed.us)

# SINTRA — Instrucciones de despliegue y ejecución

Este repositorio contiene la aplicación Django "SINTRA" (admin / remisiones / clientes, etc.). Este README describe cómo ejecutar y desplegar la aplicación en entornos de desarrollo y producción, con instrucciones enfocadas en ejecución local (sin contenedores).

Contenido
- Requisitos previos
- Ejecutar localmente (sin Docker)
- Producción recomendada (sugerida)
- wkhtmltopdf
- Seguridad y variables de entorno
- Comandos útiles

Requisitos previos
------------------
- Python 3.11
- PostgreSQL

Ejecutar localmente (sin Docker)
--------------------------------
1. Crear y activar un virtualenv:

```powershell
python -m venv env
.\env\Scripts\Activate
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Configurar `core/settings.py` o exportar la variable de entorno `DATABASE_URL` apuntando a PostgreSQL.

4. Migraciones y crear usuario admin:

```powershell
python manage.py makemigrations
python manage.py migrate
psql -U postgres -d sintra -f limpiar_permisos.sql
psql -U postgres -d sintra -f arreglar_secuencia.sql
psql -U postgres -d sintra -f scripts_permisos.sql
python crear_admin.py
```

5. Correr servidor de desarrollo:

```powershell
python manage.py runserver
```


Comandos útiles
---------------
- Instalar dependencias:

```powershell
pip install -r requirements.txt
```

- Ejecutar migraciones:

```powershell
python manage.py migrate
```

- Crear usuario admin:

```powershell
python crear_admin.py
```


Notas importantes:
- Los scripts SQL de inicialización (`scripts_permisos.sql`, `arreglar_secuencia.sql`) deben ejecutarse manualmente contra la base de datos si no usas un mecanismo de inicialización automatizado.
- Ajusta `WKHTMLTOPDF_CMD` en `core/settings.py` si el ejecutable está en una ruta distinta.

