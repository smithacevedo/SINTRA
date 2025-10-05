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

Producción recomendada (sugerida)
---------------------------------
- Utiliza un servidor de aplicaciones (Gunicorn/uvicorn) detrás de un Reverse Proxy (Nginx) para TLS, compresión y servir estáticos.
- Para media de usuarios usa un almacenamiento externo (S3/Azure Blob) y no el sistema de archivos local.
- Construye y despliega tus artefactos (imágenes, paquetes o builds) según tu estrategia de CI/CD y el entorno de destino.

wkhtmltopdf
-----------
- Asegúrate de tener `wkhtmltopdf` instalado en tu entorno si vas a usar `pdfkit`.
- Alternativas: usar headless Chrome/Playwright o un servicio de conversión si deseas evitar dependencias nativas.

Seguridad y variables de entorno
--------------------------------
No comites secretos. Antes de desplegar asegúrate de configurar las siguientes variables de entorno en tu entorno de producción:

- `SECRET_KEY` (clave secreta de Django)
- `DEBUG=False` en producción
- `DATABASE_URL` (p. ej. postgres://user:pass@host:port/dbname) — opcional si configuras `DATABASES` en `core/settings.py`
- `WKHTMLTOPDF_CMD` si el ejecutable está en otra ruta

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

Contacto y notas
----------------
Si necesitas que prepare instrucciones para despliegue con contenedores (Docker) o una configuración de `docker-compose` / `Dockerfile`, indícalo y la puedo generar. Actualmente el repositorio está documentado para ejecución local.

Comandos rápidos: backup/restore (ejemplo local)
------------------------------------------------
- Volcar la base de datos a un archivo SQL en el host:

```powershell
pg_dump -U postgres -h localhost -d sintra > sintra_backup.sql
```

- Restaurar el dump en la base de datos local o remota:

```powershell
psql -U postgres -h localhost -d sintra < sintra_backup.sql
```

Notas importantes:
- Los scripts SQL de inicialización (`scripts_permisos.sql`, `arreglar_secuencia.sql`) deben ejecutarse manualmente contra la base de datos si no usas un mecanismo de inicialización automatizado.
- Ajusta `WKHTMLTOPDF_CMD` en `core/settings.py` si el ejecutable está en una ruta distinta.

Desarrollo: cómo ajustar el código y probar cambios
-------------------------------------------------

Flujo recomendado para editar, probar y subir cambios:

1) Desarrollo local (virtualenv)

```powershell
.\env\Scripts\Activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

2) Tests

```powershell
python manage.py test
```

Buenas prácticas
----------------
- No almacenar secretos en el repo; usar variables de entorno.
- Versionar migraciones.
- Hacer backup antes de operaciones destructivas en la BD.


