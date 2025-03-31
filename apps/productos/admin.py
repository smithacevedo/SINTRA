from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'precio', 'descripcion')
    search_fields = ('referencia',)
