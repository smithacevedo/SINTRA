from django.shortcuts import render, get_object_or_404
from .models import Remision, DetalleRemision
from apps.utils.permisos import requiere_permiso
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
from django.conf import settings
import io
import datetime



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
def descargar_remision_excel(request, remision_id):
    try:
        import openpyxl
        from openpyxl.drawing.image import Image as XLImage
    except Exception:
        return HttpResponse('Instale openpyxl y Pillow para generar Excel', status=500)

    remision = get_object_or_404(Remision, id=remision_id)
    detalles = remision.detalles.filter(despacho__reintegro=False)
    core_dir = getattr(settings, 'CORE_DIR', '')
    plantilla = os.path.join(core_dir, 'apps', 'templates', 'EXCEL', 'remisiones.xlsx')

    if os.path.exists(plantilla):
        try:
            wb = openpyxl.load_workbook(plantilla)
            ws = wb['Hoja1'] if 'Hoja1' in wb.sheetnames else wb.active
        except Exception:
            wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Hoja1'
    else:
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Hoja1'

    hoy = datetime.date.today()
    ws.cell(row=1, column=6, value=f"Fecha: {hoy.day}/{hoy.month}/{hoy.year}")

    img_file = os.path.join(core_dir, 'apps', 'templates', 'IMG', 'REMISIONES.png')
    if os.path.exists(img_file):
        try:
            img = XLImage(img_file)
        except Exception:
            with open(img_file, 'rb') as f:
                img = XLImage(io.BytesIO(f.read()))
        orig_w, orig_h = getattr(img, 'width', None), getattr(img, 'height', None)
        if orig_w and orig_h:
            target_w = 420
            img.width = target_w
            img.height = int(target_w * orig_h / orig_w)
            try:
                for c in ('A', 'B', 'C', 'D'):
                    ws.column_dimensions[c].width = (target_w / 4 - 5) / 7
            except Exception:
                pass
            try:
                ws.column_dimensions['B'].width = 30
                ws.column_dimensions['C'].width = 30
            except Exception:
                pass
            try:
                h_pts = img.height * 0.75
                ws.row_dimensions[1].height = int(h_pts * 0.7)
                ws.row_dimensions[2].height = int(h_pts * 0.3)
            except Exception:
                pass
        ws.add_image(img, 'A1')
        try:
            cur_h = ws.row_dimensions[2].height
            if not cur_h:
                ws.row_dimensions[2].height = 20
            else:
                ws.row_dimensions[2].height = int(cur_h) + 8
        except Exception:
            try:
                ws.row_dimensions[2].height = 20
            except Exception:
                pass

    def _write_cell(ws, row, col, value):
        try:
            for m in ws.merged_cells.ranges:
                if m.min_row <= row <= m.max_row and m.min_col <= col <= m.max_col:
                    return ws.cell(row=m.min_row, column=m.min_col, value=value)
        except Exception:
            pass
        return ws.cell(row=row, column=col, value=value)

    destino = getattr(getattr(remision, 'orden', None), 'proyecto', None)
    nombre = destino.nombre_proyecto if destino else getattr(remision.orden, 'cliente', None)
    if hasattr(nombre, 'nombre_cliente'):
        nombre = nombre.nombre_cliente
    _write_cell(ws, 4, 2, nombre or '')

    direccion = ''
    if destino:
        direccion = getattr(destino, 'direccion_proyecto', '') or ''
    else:
        direccion = getattr(getattr(remision.orden, 'cliente', None), 'direccion_cliente', '') or ''
    _write_cell(ws, 5, 2, direccion)

    _write_cell(ws, 6, 7, getattr(getattr(remision, 'orden', None), 'codigo_oc', ''))
    _write_cell(ws, 7, 7, remision.numero_remision)

    r = 10
    for det in detalles:
        d = det.despacho
        prod_solic = getattr(d, 'producto_solicitado', None)
        referencia = getattr(getattr(prod_solic, 'producto', None), 'referencia', '')
        descripcion = getattr(prod_solic, 'descripcion', '') or getattr(getattr(prod_solic, 'producto', None), 'descripcion', '') or ''
        _write_cell(ws, r, 1, referencia)
        _write_cell(ws, r, 2, descripcion)

        talla = ''
        try:
            if referencia and '-' in referencia:
                posible = referencia.split('-')[-1].strip()
                if posible:
                    talla = posible
        except Exception:
            talla = ''

        if not talla:
            producto = getattr(prod_solic, 'producto', None)
            for attr in ('talla', 'size', 'size_code', 'size_value'):
                val = getattr(producto, attr, None) or getattr(prod_solic, attr, None)
                if val:
                    talla = str(val)
                    break

        if not talla:
            import re
            for text in (getattr(prod_solic, 'descripcion', ''), getattr(producto, 'descripcion', ''), getattr(producto, 'articulo', '')):
                if not text:
                    continue
                m = re.search(r'(?:Talla|talla|Size|size)[:\s]*([A-Za-z0-9\-\_]+)', str(text))
                if m:
                    talla = m.group(1)
                    break

        _write_cell(ws, r, 4, talla)

        _write_cell(ws, r, 5, getattr(prod_solic, 'cantidad', ''))
        _write_cell(ws, r, 6, getattr(d, 'cantidad', ''))
        _write_cell(ws, r, 7, getattr(prod_solic, 'pendiente', ''))
        r += 1

    out = io.BytesIO(); wb.save(out); out.seek(0)
    fn = f"remision_{remision.numero_remision}.xlsx"
    resp = HttpResponse(out.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    resp['Content-Disposition'] = f'attachment; filename="{fn}"'
    return resp