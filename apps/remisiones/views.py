import platform
import shutil
from django.shortcuts import render, get_object_or_404
from .models import Remision, DetalleRemision
from apps.utils.permisos import requiere_permiso
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
from django.conf import settings
import io
import datetime
import openpyxl
from openpyxl.drawing.image import Image as XLImage
import subprocess
import tempfile
from openpyxl.worksheet.page import PageMargins



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

    remision = get_object_or_404(Remision, id=remision_id)
    detalles = remision.detalles.filter(despacho__reintegro=False)
    core_dir = getattr(settings, 'CORE_DIR', '')
    plantilla = os.path.join(core_dir, 'apps', 'templates', 'EXCEL', 'remisiones.xlsx')

    if os.path.exists(plantilla):
        wb = openpyxl.load_workbook(plantilla)
        ws = wb['Hoja1'] if 'Hoja1' in wb.sheetnames else wb.active
    else:
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Hoja1'

    def _write_cell(ws, row, col, value):
        for m in ws.merged_cells.ranges:
            if m.min_row <= row <= m.max_row and m.min_col <= col <= m.max_col:
                return ws.cell(row=m.min_row, column=m.min_col, value=value)
        return ws.cell(row=row, column=col, value=value)

    def _get_city_name(val):
        if not val:
            return ''
        if isinstance(val, str):
            return val.split(',')[0].strip()
        for attr in ('name', 'nombre', 'nombre_ciudad', 'city_name', 'ciudad'):
            v = getattr(val, attr, None)
            if v:
                return str(v).split(',')[0].strip()
        try:
            return str(val).split(',')[0].strip()
        except Exception:
            return ''

    hoy = datetime.date.today()
    _write_cell(ws, 4, 7, f"{hoy.day}/{hoy.month}/{hoy.year}")

    img_file = os.path.join(core_dir, 'apps', 'templates', 'IMG', 'REMISIONES.png')
    if os.path.exists(img_file):
        img = XLImage(img_file)
        orig_w, orig_h = getattr(img, 'width', None), getattr(img, 'height', None)
        if orig_w and orig_h:
            target_w = 420
            img.width = target_w
            img.height = int(target_w * orig_h / orig_w)
            ws.column_dimensions['A'].width = 18
            ws.column_dimensions['B'].width = 30
            ws.column_dimensions['C'].width = 30
            ws.column_dimensions['D'].width = 18
            h_pts = img.height * 0.75
            ws.row_dimensions[1].height = int(h_pts * 0.7)
            ws.row_dimensions[2].height = int(h_pts * 0.3)
        ws.add_image(img, 'A1')
        cur_h = ws.row_dimensions[2].height
        if not cur_h:
            ws.row_dimensions[2].height = 20
        else:
            ws.row_dimensions[2].height = int(cur_h) + 8


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

    telefono = ''
    if destino:
        telefono = getattr(destino, 'telefono_contacto', '') or ''
    else:
        telefono = getattr(getattr(remision.orden, 'cliente', None), 'telefono_contacto', '') or ''
    _write_cell(ws, 5, 7, telefono)

    ciudad = ''
    if destino:
        ciudad = getattr(destino, 'ciudad_proyecto', '') or ''
    else:
        ciudad = getattr(getattr(remision.orden, 'cliente', None), 'ciudad_cliente', '') or ''
    ciudad = _get_city_name(ciudad)
    _write_cell(ws, 6, 2, ciudad)

    nombre_contacto = ''
    if destino:
        nombre_contacto = getattr(destino, 'nombre_contacto', '') or ''
    else:
        nombre_contacto = getattr(getattr(remision.orden, 'cliente', None), 'nombre_contacto', '') or ''
    _write_cell(ws, 7, 2, nombre_contacto)

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
        if referencia and '-' in referencia:
            posible = referencia.split('-')[-1].strip()
            if posible:
                talla = posible

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


# --- PDF desde Excel usando LibreOffice (soffice) ---
@requiere_permiso('ver_remisiones')
def descargar_remision_pdf(request, remision_id):
    remision = get_object_or_404(Remision, id=remision_id)
    detalles = remision.detalles.filter(despacho__reintegro=False)
    core_dir = getattr(settings, 'CORE_DIR', '')
    plantilla = os.path.join(core_dir, 'apps', 'templates', 'EXCEL', 'remisiones.xlsx')

    if os.path.exists(plantilla):
        wb = openpyxl.load_workbook(plantilla)
        ws = wb['Hoja1'] if 'Hoja1' in wb.sheetnames else wb.active
    else:
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Hoja1'

    def _write_cell(ws, row, col, value):
        for m in ws.merged_cells.ranges:
            if m.min_row <= row <= m.max_row and m.min_col <= col <= m.max_col:
                return ws.cell(row=m.min_row, column=m.min_col, value=value)
        return ws.cell(row=row, column=col, value=value)

    def _get_city_name(val):
        if not val:
            return ''
        if isinstance(val, str):
            return val.split(',')[0].strip()
        for attr in ('name', 'nombre', 'nombre_ciudad', 'city_name', 'ciudad'):
            v = getattr(val, attr, None)
            if v:
                return str(v).split(',')[0].strip()
        try:
            return str(val).split(',')[0].strip()
        except Exception:
            return ''

    hoy = datetime.date.today()
    _write_cell(ws, 4, 7, f"{hoy.day}/{hoy.month}/{hoy.year}")

    img_file = os.path.join(core_dir, 'apps', 'templates', 'IMG', 'REMISIONES.png')
    if os.path.exists(img_file):
        img = XLImage(img_file)
        orig_w, orig_h = getattr(img, 'width', None), getattr(img, 'height', None)
        if orig_w and orig_h:
            target_w = 420
            img.width = target_w
            img.height = int(target_w * orig_h / orig_w)
            ws.column_dimensions['A'].width = 18
            ws.column_dimensions['B'].width = 30
            ws.column_dimensions['C'].width = 30
            ws.column_dimensions['D'].width = 18
            h_pts = img.height * 0.75
            ws.row_dimensions[1].height = int(h_pts * 0.7)
            ws.row_dimensions[2].height = int(h_pts * 0.3)
        ws.add_image(img, 'A1')
        cur_h = ws.row_dimensions[2].height
        if not cur_h:
            ws.row_dimensions[2].height = 20
        else:
            ws.row_dimensions[2].height = int(cur_h) + 8

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

    telefono = ''
    if destino:
        telefono = getattr(destino, 'telefono_contacto', '') or ''
    else:
        telefono = getattr(getattr(remision.orden, 'cliente', None), 'telefono_contacto', '') or ''
    _write_cell(ws, 5, 7, telefono)

    ciudad = ''
    if destino:
        ciudad = getattr(destino, 'ciudad_proyecto', '') or ''
    else:
        ciudad = getattr(getattr(remision.orden, 'cliente', None), 'ciudad_cliente', '') or ''
    ciudad = _get_city_name(ciudad)
    _write_cell(ws, 6, 2, ciudad)

    nombre_contacto = ''
    if destino:
        nombre_contacto = getattr(destino, 'nombre_contacto', '') or ''
    else:
        nombre_contacto = getattr(getattr(remision.orden, 'cliente', None), 'nombre_contacto', '') or ''
    _write_cell(ws, 7, 2, nombre_contacto)

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
        if referencia and '-' in referencia:
            posible = referencia.split('-')[-1].strip()
            if posible:
                talla = posible

        _write_cell(ws, r, 4, talla)

        _write_cell(ws, r, 5, getattr(prod_solic, 'cantidad', ''))
        _write_cell(ws, r, 6, getattr(d, 'cantidad', ''))
        _write_cell(ws, r, 7, getattr(prod_solic, 'pendiente', ''))
        r += 1

        # Tamaño carta y orientación
        ws.page_setup.paperSize = 1                # PAPERSIZE_LETTER
        ws.page_setup.orientation = 'portrait'

        # Ajustar a 1 página
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 1

        # Márgenes (en pulgadas) y centrado
        ws.page_margins = PageMargins(left=0.25, right=0.25, top=0.5, bottom=0.5,
                                    header=0.3, footer=0.3)
        ws.print_options.horizontalCentered = True

    # Guardar Excel temporalmente y convertir a PDF con LibreOffice
    with tempfile.TemporaryDirectory() as tmpdir:
        excel_path = os.path.join(tmpdir, f'remision_{remision.numero_remision}.xlsx')
        pdf_path = os.path.join(tmpdir, f'remision_{remision.numero_remision}.pdf')
        wb.save(excel_path)

        # Buscar ruta de soffice según sistema operativo
        soffice_path = os.environ.get('SOFFICE_PATH')
        if not soffice_path:
            soffice_path = shutil.which('soffice')

        if platform.system() == 'Linux' and os.path.exists('/usr/bin/soffice'):
            soffice_path = '/usr/bin/soffice'

        if not soffice_path:
            raise FileNotFoundError("No se encontró LibreOffice (soffice). Ajusta la variable SOFFICE_PATH o instala LibreOffice.")

        # Convertir a PDF
        subprocess.run([
            soffice_path, '--headless', '--convert-to', 'pdf', excel_path, '--outdir', tmpdir
        ], check=True)

        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="remision_{remision.numero_remision}.pdf"'
        return response