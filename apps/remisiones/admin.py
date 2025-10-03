from django.contrib import admin
from .models import Remision, DetalleRemision


@admin.register(Remision)
class RemisionAdmin(admin.ModelAdmin):
    list_display = ['numero_remision', 'orden', 'fecha_remision']
    readonly_fields = ['numero_remision']


@admin.register(DetalleRemision)
class DetalleRemisionAdmin(admin.ModelAdmin):
    list_display = ['remision', 'despacho']