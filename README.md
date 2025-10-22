```bash
< SINTRA PROJECT ROOT >
   |
   |-- core/                               # Configuración principal de Django
   |    |-- settings.py                    # Configuración global del proyecto
   |    |-- wsgi.py                        # Servidor WSGI para producción
   |    |-- urls.py                        # URLs principales del proyecto
   |    |-- asgi.py                        # Servidor ASGI para aplicaciones async
   |
   |-- apps/                               # Aplicaciones del sistema SINTRA
   |    |
   |    |-- authentication/                # Autenticación y autorización
   |    |    |-- views.py                  # Vistas de login/registro
   |    |    |-- urls.py                   # Rutas de autenticación
   |    |    |-- forms.py                  # Formularios de auth
   |    |
   |    |-- home/                          # Página principal y dashboard
   |    |    |-- views.py                  # Vista del dashboard
   |    |    |-- urls.py                   # Rutas principales
   |    |
   |    |-- clientes/                      # Gestión de clientes
   |    |    |-- models.py                 # Modelo Cliente
   |    |    |-- views.py                  # CRUD de clientes
   |    |    |-- forms.py                  # Formularios de cliente
   |    |    |-- urls.py                   # Rutas de clientes
   |    |
   |    |-- productos/                     # Gestión de productos
   |    |    |-- models.py                 # Modelo Producto
   |    |    |-- views.py                  # CRUD de productos
   |    |    |-- forms.py                  # Formularios de producto
   |    |    |-- urls.py                   # Rutas de productos
   |    |
   |    |-- proveedores/                   # Gestión de proveedores
   |    |    |-- models.py                 # Modelo Proveedor
   |    |    |-- views.py                  # CRUD de proveedores
   |    |    |-- forms.py                  # Formularios de proveedor
   |    |    |-- urls.py                   # Rutas de proveedores
   |    |
   |    |-- proyectos/                     # Gestión de proyectos
   |    |    |-- models.py                 # Modelo Proyecto
   |    |    |-- views.py                  # CRUD de proyectos
   |    |    |-- forms.py                  # Formularios de proyecto
   |    |    |-- urls.py                   # Rutas de proyectos
   |    |
   |    |-- ordenes_compra/                # Órdenes de compra
   |    |    |-- models.py                 # Modelos OrdenCompra, DetalleOrden
   |    |    |-- views.py                  # CRUD de órdenes
   |    |    |-- forms.py                  # Formularios de órdenes
   |    |    |-- urls.py                   # Rutas de órdenes
   |    |
   |    |-- remisiones/                    # Remisiones de productos
   |    |    |-- models.py                 # Modelos Remision, DetalleRemision
   |    |    |-- views.py                  # Gestión de remisiones
   |    |    |-- urls.py                   # Rutas de remisiones
   |    |
   |    |-- despachos/                     # Control de despachos
   |    |    |-- models.py                 # Modelo Despacho
   |    |    |-- views.py                  # Gestión de despachos
   |    |    |-- urls.py                   # Rutas de despachos
   |    |
   |    |-- usuarios/                      # Gestión de usuarios del sistema
   |    |    |-- models.py                 # Modelo Usuario personalizado
   |    |    |-- views.py                  # CRUD de usuarios
   |    |    |-- forms.py                  # Formularios de usuario
   |    |    |-- middleware.py             # Middleware personalizado
   |    |    |-- urls.py                   # Rutas de usuarios
   |    |
   |    |-- roles/                         # Sistema de roles
   |    |    |-- models.py                 # Modelo Rol
   |    |    |-- views.py                  # Gestión de roles
   |    |    |-- forms.py                  # Formularios de roles
   |    |    |-- urls.py                   # Rutas de roles
   |    |
   |    |-- permisos/                      # Sistema de permisos
   |    |    |-- models.py                 # Modelo Permiso
   |    |    |-- views.py                  # Gestión de permisos
   |    |    |-- forms.py                  # Formularios de permisos
   |    |    |-- urls.py                   # Rutas de permisos
   |    |
   |    |-- utils/                         # Utilidades del sistema
   |    |    |-- context_processors.py     # Procesadores de contexto
   |    |    |-- mixins.py                 # Mixins reutilizables
   |    |    |-- permisos.py               # Decoradores de permisos
   |    |
   |    |-- static/                        # Archivos estáticos
   |    |    |-- assets/                   # CSS, JS, imágenes
   |    |
   |    |-- templates/                     # Plantillas HTML
   |         |-- layouts/                  # Plantillas base
   |         |    |-- base.html            # Layout principal
   |         |    |-- base-fullscreen.html # Layout pantalla completa
   |         |
   |         |-- includes/                 # Componentes reutilizables
   |         |    |-- navigation.html      # Menú de navegación
   |         |    |-- sidebar.html         # Barra lateral
   |         |    |-- footer.html          # Pie de página
   |         |    |-- scripts.html         # Scripts comunes
   |         |
   |         |-- accounts/                 # Páginas de autenticación
   |         |-- home/                     # Páginas principales
   |         |-- clientes/                 # Templates de clientes
   |         |-- productos/                # Templates de productos
   |         |-- proveedores/              # Templates de proveedores
   |         |-- proyectos/                # Templates de proyectos
   |         |-- ordenes_compra/           # Templates de órdenes
   |         |-- remisiones/               # Templates de remisiones
   |         |-- despachos/                # Templates de despachos
   |         |-- usuarios/                 # Templates de usuarios
   |         |-- roles/                    # Templates de roles
   |         |-- permisos/                 # Templates de permisos
   |         |-- EXCEL/                    # Templates para Excel
   |
   |-- media/                              # Archivos multimedia
   |-- staticfiles/                        # Archivos estáticos compilados
   |-- nginx/                              # Configuración Nginx
   |
   |-- requirements.txt                    # Dependencias Python
   |-- .env                                # Variables de entorno
   |-- manage.py                           # Script de gestión Django
   |-- crear_admin.py                      # Script para crear admin
   |-- scripts_permisos.sql                # Script de permisos SQL
   |-- limpiar_permisos.sql                # Script limpieza permisos
   |-- arreglar_secuencia.sql              # Script arreglo secuencias
   |-- clear_migrations.py                 # Script limpiar migraciones
   |-- gunicorn-cfg.py                     # Configuración Gunicorn
```



## Licensing

- Copyright 2019 - present [Creative Tim](https://www.creative-tim.com/)
- Licensed under [Creative Tim EULA](https://www.creative-tim.com/license)


---
[Material Dashboard Django](https://www.creative-tim.com/product/material-dashboard-django) - Provided by [Creative Tim](https://www.creative-tim.com/) and [AppSeed](https://appseed.us)

# SINTRA — Instrucciones de despliegue y ejecución

SINTRA es un sistema integral de gestión empresarial desarrollado en Django que incluye:

- **Gestión de Clientes**: Registro y administración de información de clientes
- **Gestión de Productos**: Catálogo de productos con códigos y especificaciones
- **Gestión de Proveedores**: Administración de proveedores y contactos
- **Gestión de Proyectos**: Control de proyectos empresariales
- **Órdenes de Compra**: Creación y seguimiento de órdenes de compra
- **Remisiones**: Generación de remisiones con exportación a Excel
- **Control de Despachos**: Seguimiento de entregas y despachos
- **Sistema de Usuarios**: Gestión completa de usuarios con roles y permisos
- **Sistema de Roles y Permisos**: Control granular de accesos

Este README describe cómo ejecutar y desplegar la aplicación en entornos de desarrollo y producción.

## Contenido
- [Requisitos previos](#requisitos-previos)
- [Ejecutar localmente](#ejecutar-localmente-sin-docker)
- [Comandos útiles](#comandos-útiles)
- [Funcionalidades principales](#funcionalidades-principales)
- [Estructura del proyecto](#estructura-del-proyecto)

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


## Funcionalidades Principales

### Módulos Implementados
- ✅ **Autenticación**: Login/logout con sistema de sesiones
- ✅ **Dashboard**: Página principal con resumen del sistema
- ✅ **Clientes**: CRUD completo con búsqueda y filtros
- ✅ **Productos**: Gestión de catálogo de productos
- ✅ **Proveedores**: Administración de proveedores
- ✅ **Proyectos**: Control de proyectos empresariales
- ✅ **Órdenes de Compra**: Creación y gestión de órdenes
- ✅ **Remisiones**: Generación con exportación Excel
- ✅ **Despachos**: Control de entregas
- ✅ **Usuarios**: Sistema completo de usuarios
- ✅ **Roles y Permisos**: Control de accesos granular

### Características Técnicas
- **Base de Datos**: PostgreSQL
- **Framework**: Django 4.x
- **Frontend**: Material Dashboard (Bootstrap)
- **Exportación**: Excel (openpyxl)
- **Autenticación**: Sistema Django personalizado
- **Permisos**: Sistema de roles y permisos granular

## Notas Importantes
- Los scripts SQL de inicialización (`scripts_permisos.sql`, `arreglar_secuencia.sql`, `limpiar_permisos.sql`) deben ejecutarse manualmente contra la base de datos
- El sistema incluye middleware personalizado para control de permisos
- Las remisiones se pueden exportar a Excel (funcionalidad PDF removida)
- El sistema utiliza un modelo de usuario personalizado

