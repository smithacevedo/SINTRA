from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Permiso
from .forms import PermisoForm
from apps.utils.permisos import requiere_permiso, tiene_permiso


def lista_permisos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not tiene_permiso(request.user, 'ver_permisos'):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('home')
    
    solo_lectura = not (tiene_permiso(request.user, 'crear_permisos') or 
                       tiene_permiso(request.user, 'editar_permisos') or 
                       tiene_permiso(request.user, 'eliminar_permisos'))
    permisos = Permiso.objects.all().order_by('id')
    
    paginator = Paginator(permisos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'permisos/lista_permisos.html', {
        'permisos': page_obj,
        'page_obj': page_obj,
        'solo_lectura': solo_lectura
    })


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