import os
import django
from django.db import connection, transaction
from django.contrib.auth import get_user_model

# Configurar entorno Django si se ejecuta fuera de manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Importar modelos
from apps.permisos.models import Permiso
from apps.roles.models import Rol
from django.contrib.auth.models import User
from apps.usuarios.models import UsuarioRol, PerfilUsuario

User = get_user_model()


def reset_roles_y_permisos():
    """Limpia tablas de permisos, roles y usuarios (excepto superusers) y vuelve a sembrar datos base."""
    PERMISOS_SEED = [
        ("Ver Dashboard", "ver_dashboard"),
        ("Ver Productos", "ver_productos"),
        ("Crear Productos", "crear_productos"),
        ("Editar Productos", "editar_productos"),
        ("Eliminar Productos", "eliminar_productos"),
        ("Ver Clientes", "ver_clientes"),
        ("Crear Clientes", "crear_clientes"),
        ("Editar Clientes", "editar_clientes"),
        ("Eliminar Clientes", "eliminar_clientes"),
        ("Ver Pedidos", "ver_pedidos"),
        ("Crear Pedidos", "crear_pedidos"),
        ("Editar Pedidos", "editar_pedidos"),
        ("Eliminar Pedidos", "eliminar_pedidos"),
        ("Ver Despachos", "ver_despachos"),
        ("Crear Despachos", "crear_despachos"),
        ("Editar Despachos", "editar_despachos"),
        ("Ver Remisiones", "ver_remisiones"),
        ("Crear Remisiones", "crear_remisiones"),
        ("Editar Remisiones", "editar_remisiones"),
        ("Ver Usuarios", "ver_usuarios"),
        ("Crear Usuarios", "crear_usuarios"),
        ("Editar Usuarios", "editar_usuarios"),
        ("Eliminar Usuarios", "eliminar_usuarios"),
        ("Ver Roles", "ver_roles"),
        ("Crear Roles", "crear_roles"),
        ("Editar Roles", "editar_roles"),
        ("Eliminar Roles", "eliminar_roles"),
        ("Ver Permisos", "ver_permisos"),
        ("Crear Permisos", "crear_permisos"),
        ("Editar Permisos", "editar_permisos"),
        ("Eliminar Permisos", "eliminar_permisos"),
    ]

    ROLES_SEED = ["Administrador", "Gerente", "Operador", "Consultor"]

    print("🔄 Iniciando reseteo de roles y permisos...")

    with transaction.atomic():
        # Eliminar relaciones y datos
        _delete_relations_and_profiles()

        Rol.objects.all().delete()
        Permiso.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Reiniciar secuencias
        _reset_sequences([
            ("permisos_permiso", "id"),
            ("roles_rol", "id"),
            ("auth_user", "id"),
        ])

        # Crear permisos
        permisos = [Permiso(nombre=n, llave=l) for n, l in PERMISOS_SEED]
        Permiso.objects.bulk_create(permisos)
        print(f"✅ Permisos creados: {Permiso.objects.count()}")

        # Crear roles
        roles = [Rol(nombre=r) for r in ROLES_SEED]
        Rol.objects.bulk_create(roles)
        print(f"✅ Roles creados: {Rol.objects.count()}")

        # Asignar permisos
        permisos_qs = Permiso.objects.all()
        rol_admin = Rol.objects.get(nombre="Administrador")
        rol_gerente = Rol.objects.get(nombre="Gerente")
        rol_operador = Rol.objects.get(nombre="Operador")
        rol_consultor = Rol.objects.get(nombre="Consultor")

        rol_admin.permisos.set(permisos_qs)

        rol_gerente.permisos.set(permisos_qs.filter(llave__in={
            'ver_dashboard', 'ver_productos', 'crear_productos', 'editar_productos',
            'ver_clientes', 'crear_clientes', 'editar_clientes',
            'ver_pedidos', 'crear_pedidos', 'editar_pedidos'
        }))

        rol_operador.permisos.set(permisos_qs.filter(llave__in={
            'ver_dashboard', 'ver_despachos', 'crear_despachos', 'editar_despachos',
            'ver_remisiones', 'crear_remisiones', 'editar_remisiones'
        }))

        rol_consultor.permisos.set(permisos_qs.filter(llave__in={
            'ver_dashboard', 'ver_productos', 'ver_clientes', 'ver_pedidos',
            'ver_despachos', 'ver_remisiones'
        }))

        _bump_sequence_to_max_plus_one("auth_user", "id")
        crear_usuario_admin()

    print("🎉 Script completado con éxito.")


def _delete_relations_and_profiles():
    """Limpia relaciones y tablas auxiliares si existen."""
    with connection.cursor() as cur:
        for table in ["usuario_rol", "perfil_usuario", "roles_rol_permisos"]:
            try:
                cur.execute(f'DELETE FROM "{table}";')
                print(f"🧹 Limpieza OK -> {table}")
            except Exception:
                print(f"(tabla {table} no existe, omitida)")


def _reset_sequences(table_cols):
    """Reinicia secuencias a 1."""
    with connection.cursor() as cur:
        for table, col in table_cols:
            cur.execute("SELECT pg_get_serial_sequence(%s, %s);", [f'"{table}"', col])
            row = cur.fetchone()
            if row and row[0]:
                seq = row[0]
                cur.execute(f"ALTER SEQUENCE {seq} RESTART WITH 1;")
                print(f"🔁 Secuencia reiniciada: {seq}")
            else:
                print(f"(sin secuencia para {table}.{col})")


def _bump_sequence_to_max_plus_one(table, col):
    """Ajusta secuencia a MAX(id)+1."""
    with connection.cursor() as cur:
        cur.execute("SELECT pg_get_serial_sequence(%s, %s);", [f'"{table}"', col])
        row = cur.fetchone()
        if not row or not row[0]:
            return
        seq = row[0]
        cur.execute(f"SELECT COALESCE(MAX({col}), 0) FROM \"{table}\";")
        max_id = cur.fetchone()[0] or 0
        cur.execute("SELECT setval(%s, %s, %s);", [seq, max_id + 1, True])
        print(f"⚙️ Secuencia ajustada: {seq} → {max_id + 1}")


def crear_usuario_admin():
    # Crear usuario
    usuario, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'email': 'admin@sintra.com',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True
        }
    )

    if created:
        usuario.set_password('admin123')
        usuario.save()
        print(f"Usuario '{usuario.username}' creado exitosamente")
    else:
        print(f"Usuario '{usuario.username}' ya existe")

    # Crear perfil
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={'primer_acceso': False}
    )

    if created:
        print("Perfil de usuario creado")

    # Asignar rol Administrador
    try:
        rol_admin = Rol.objects.get(nombre='Administrador')
        usuario_rol, created = UsuarioRol.objects.get_or_create(
            usuario=usuario,
            rol=rol_admin
        )

        if created:
            print("Rol Administrador asignado")
        else:
            print("Rol Administrador ya estaba asignado")

    except Rol.DoesNotExist:
        print("ERROR: Rol 'Administrador' no existe. Ejecuta primero el script SQL.")
        return

    print("\n=== USUARIO ADMINISTRADOR ===")
    print(f"Usuario: {usuario.username}")
    print(f"Contraseña: admin123")
    print(f"Email: {usuario.email}")
    print("Acceso: COMPLETO")

if __name__ == "__main__":
    reset_roles_y_permisos()
