from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Rol
from .forms import RolForm


def lista_roles(request):
    roles = Rol.objects.all().order_by('nombre')
    return render(request, 'roles/lista_roles.html', {'roles': roles})


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


def eliminar_rol(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)
    rol.delete()
    messages.success(request, 'Rol eliminado exitosamente.')
    return redirect('lista_roles')