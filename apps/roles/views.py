from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Rol
from .forms import RolForm
from apps.utils.permisos import requiere_permiso


@requiere_permiso('ver_roles')
def lista_roles(request):
    roles = Rol.objects.all().order_by('nombre')
    return render(request, 'roles/lista_roles.html', {'roles': roles})


@requiere_permiso('crear_roles')
def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol creado exitosamente.')
            return redirect('lista_roles')
    else:
        form = RolForm()
    
    return render(request, 'roles/crear_rol.html', {'form': form})


@requiere_permiso('editar_roles')
def editar_rol(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)
    
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol actualizado exitosamente.')
            return redirect('lista_roles')
    else:
        form = RolForm(instance=rol)
    
    return render(request, 'roles/editar_rol.html', {'form': form, 'rol': rol})


@requiere_permiso('eliminar_roles')
def eliminar_rol(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)
    rol.delete()
    messages.success(request, 'Rol eliminado exitosamente.')
    return redirect('lista_roles')