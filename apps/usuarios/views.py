from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from apps.roles.models import Rol
from apps.permisos.models import Permiso
from .models import UsuarioRol, PerfilUsuario
from .forms import UsuarioForm
from apps.utils.permisos import requiere_permiso, tiene_permiso


def lista_usuarios(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not tiene_permiso(request.user, 'ver_usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    solo_lectura = not (tiene_permiso(request.user, 'crear_usuarios') or 
                       tiene_permiso(request.user, 'editar_usuarios') or 
                       tiene_permiso(request.user, 'eliminar_usuarios'))
    usuarios = User.objects.all().order_by('username')
    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'solo_lectura': solo_lectura
    })


@requiere_permiso('crear_usuarios')
def crear_usuario(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debug
        form = UsuarioForm(request.POST)
        print("Form is valid:", form.is_valid())  # Debug
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug
        
        if form.is_valid():
            try:
                usuario = form.save()
                print(f"Usuario creado: {usuario.username}")  # Debug
                
                # Crear perfil de usuario
                PerfilUsuario.objects.create(usuario=usuario, primer_acceso=True)
                print("Perfil creado")  # Debug
                
                # Asignar roles seleccionados
                roles_ids = request.POST.getlist('roles')
                print(f"Roles IDs: {roles_ids}")  # Debug
                
                for rol_id in roles_ids:
                    if rol_id:  # Verificar que no esté vacío
                        try:
                            rol = Rol.objects.get(id=rol_id)
                            UsuarioRol.objects.create(usuario=usuario, rol=rol)
                            print(f"Rol asignado: {rol.nombre}")  # Debug
                        except Rol.DoesNotExist:
                            print(f"Rol no encontrado: {rol_id}")  # Debug
                
                messages.success(request, 'Usuario creado exitosamente.')
                return redirect('lista_usuarios')
            except Exception as e:
                print(f"Error en creación: {str(e)}")  # Debug
                messages.error(request, f'Error al crear usuario: {str(e)}')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UsuarioForm()
    
    roles = Rol.objects.all()
    return render(request, 'usuarios/crear_usuario.html', {
        'form': form,
        'roles': roles
    })


@requiere_permiso('editar_usuarios')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.is_active = 'is_active' in request.POST
        usuario.save()
        
        # Actualizar roles
        UsuarioRol.objects.filter(usuario=usuario).delete()
        roles_ids = request.POST.getlist('roles')
        for rol_id in roles_ids:
            rol = Rol.objects.get(id=rol_id)
            UsuarioRol.objects.create(usuario=usuario, rol=rol)
            
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('lista_usuarios')
    
    roles = Rol.objects.all()
    roles_asignados = UsuarioRol.objects.filter(usuario=usuario).values_list('rol_id', flat=True)
    
    return render(request, 'usuarios/editar_usuario.html', {
        'usuario': usuario,
        'roles': roles,
        'roles_asignados': list(roles_asignados)
    })


@requiere_permiso('eliminar_usuarios')
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if usuario != request.user:  # No permitir eliminar el usuario actual
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
    return redirect('lista_usuarios')


@login_required
def cambiar_password_obligatorio(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 and password2:
            if password1 == password2:
                if len(password1) >= 8:
                    request.user.set_password(password1)
                    request.user.save()
                    
                    # Marcar que ya no es primer acceso
                    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
                    perfil.primer_acceso = False
                    perfil.save()
                    
                    # Mantener la sesión activa
                    update_session_auth_hash(request, request.user)
                    
                    messages.success(request, 'Contraseña cambiada exitosamente.')
                    return redirect('home')
                else:
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        else:
            messages.error(request, 'Debe completar ambos campos.')
    
    return render(request, 'usuarios/cambiar_password.html')