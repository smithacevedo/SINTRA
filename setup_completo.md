# Setup Completo - Roles y Usuarios SINTRA

## 1. Limpiar todo
```sql
-- Ejecutar en PostgreSQL
\i limpiar_permisos.sql
```

## 2. Arreglar secuencias
```sql
-- Ejecutar en PostgreSQL
\i arreglar_secuencia.sql
```

## 3. Crear permisos y roles
```sql
-- Ejecutar en PostgreSQL
\i scripts_permisos.sql
```

## 4. Crear usuario administrador
```bash
# Ejecutar en terminal
python crear_admin.py
```

## 5. Verificar funcionamiento
- Usuario: `admin`
- Contraseña: `admin123`
- Acceso: http://127.0.0.1:8000/login/

## Orden de ejecución completo:
```bash
# 1. Conectar a PostgreSQL
psql -U postgres -d sintra

# 2. Dentro de PostgreSQL ejecutar:
\i limpiar_permisos.sql
\i arreglar_secuencia.sql
\i scripts_permisos.sql
\q

# 3. En terminal del proyecto:
python crear_admin.py

# 4. Iniciar servidor:
python manage.py runserver
```