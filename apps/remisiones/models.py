from django.db import models
from apps.despachos.models import Despacho
from apps.ordenes_compra.models import OrdenCompra


class Remision(models.Model):
    numero_remision = models.CharField(max_length=20, unique=True)
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='remisiones')
    fecha_remision = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_remision:
            ultimo = Remision.objects.order_by('-id').first()
            numero = 1 if not ultimo else int(ultimo.numero_remision.split('-')[1]) + 1
            self.numero_remision = f"REM-{numero}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Remisión {self.numero_remision}"


class DetalleRemision(models.Model):
    remision = models.ForeignKey(Remision, on_delete=models.CASCADE, related_name='detalles')
    despacho = models.OneToOneField(Despacho, on_delete=models.CASCADE, related_name='remision_detalle')
    
    def __str__(self):
        return f"{self.remision.numero_remision} - {self.despacho.producto_solicitado.producto.referencia}"