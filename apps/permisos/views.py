from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Permiso
from .forms import PermisoForm
from apps.utils.permisos import requiere_permiso


@requiere_permiso('ver_permisos')
def lista_permisos(request):
    permisos = Permiso.objects.all().order_by('nombre')
    return render(request, 'permisos/lista_permisos.html', {'permisos': permisos})


@requiere_permiso('crear_permisos')
def crear_permiso(request):
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permiso creado exitosamente.')
            return redirect('lista_permisos')
    else:
        form = PermisoForm()
    
    return render(request, 'permisos/crear_permiso.html', {'form': form})


@requiere_permiso('editar_permisos')
def editar_permiso(request, permiso_id):
    permiso = get_object_or_404(Permiso, id=permiso_id)
    
    if request.method == 'POST':
        form = PermisoForm(request.POST, instance=permiso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permiso actualizado exitosamente.')
            return redirect('lista_permisos')
    else:
        form = PermisoForm(instance=permiso)
    
    return render(request, 'permisos/editar_permiso.html', {'form': form, 'permiso': permiso})


@requiere_permiso('eliminar_permisos')
def eliminar_permiso(request, permiso_id):
    permiso = get_object_or_404(Permiso, id=permiso_id)
    permiso.delete()
    messages.success(request, 'Permiso eliminado exitosamente.')
    return redirect('lista_permisos')