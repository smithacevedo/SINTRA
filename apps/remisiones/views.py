from django.shortcuts import render, get_object_or_404
from .models import Remision, DetalleRemision
from apps.utils.permisos import requiere_permiso
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
from django.conf import settings

# Usamos pdfkit (wkhtmltopdf). Si pdfkit no está instalado, la vista devolverá
# instrucciones para instalar las dependencias necesarias.
try:
    import pdfkit
    HAVE_PDFKIT = True
except Exception:
    HAVE_PDFKIT = False


@requiere_permiso('ver_remisiones')
def lista_remisiones(request):
    buscar = request.GET.get('buscar', '')
    if buscar:
        remisiones = Remision.objects.filter(numero_remision__icontains=buscar).order_by('-fecha_remision')
    else:
        remisiones = Remision.objects.all().order_by('-fecha_remision')
    
    return render(request, 'remisiones/lista_remisiones.html', {
        'remisiones': remisiones,
        'buscar': buscar
    })


@requiere_permiso('ver_remisiones')
def detalle_remision(request, remision_id):
    remision = get_object_or_404(Remision, id=remision_id)
    detalles = remision.detalles.filter(despacho__reintegro=False)
    return render(request, 'remisiones/detalle_remision.html', {
        'remision': remision,
        'detalles': detalles
    })


@requiere_permiso('ver_remisiones')
def descargar_remision(request, remision_id):
    """Genera y devuelve un PDF de la remisión.

    Implementación sencilla con xhtml2pdf. Si no está instalado, devuelve
    un mensaje indicando que hay que instalar la dependencia.
    """
    remision = get_object_or_404(Remision, id=remision_id)
    detalles = remision.detalles.filter(despacho__reintegro=False)

    # Renderizamos la plantilla HTML a string
    html = render_to_string('remisiones/remision_pdf.html', {
        'remision': remision,
        'detalles': detalles,
    })

    if not HAVE_PDFKIT:
        return HttpResponse(
            'Para generar PDFs se requiere instalar pdfkit y el binario wkhtmltopdf.\n'
            '1) pip install pdfkit\n'
            '2) instalar wkhtmltopdf desde https://wkhtmltopdf.org/downloads.html\n'
            '3) opcionalmente definir WKHTMLTOPDF_CMD en settings.py o como variable de entorno\n',
            status=500
        )

    # Intentamos generar el PDF con wkhtmltopdf
    wkhtml_cmd = getattr(settings, 'WKHTMLTOPDF_CMD', None) or os.environ.get('WKHTMLTOPDF_CMD')
    try:
        if wkhtml_cmd:
            config = pdfkit.configuration(wkhtmltopdf=wkhtml_cmd)
            pdf_bytes = pdfkit.from_string(html, False, configuration=config)
        else:
            pdf_bytes = pdfkit.from_string(html, False)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"remision_{remision.numero_remision}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except OSError:
        return HttpResponse(
            'wkhtmltopdf no encontrado o no ejecutable. Asegúrate de instalar wkhtmltopdf y que la ruta esté en PATH, '
            'o define WKHTMLTOPDF_CMD en settings.py con la ruta completa al ejecutable.',
            status=500
        )
    except Exception as e:
        return HttpResponse(f'Error al generar PDF: {e}', status=500)