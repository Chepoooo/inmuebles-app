from io import BytesIO
from html import escape
from urllib.request import Request, urlopen
import certifi
import ssl
from django.utils.timezone import localtime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .defaults import KEYS_SECTION_NAME


# ============================================================
# TEXTO
# ============================================================

def _safe_text(value, default="No registrado"):
    """
    Convierte cualquier valor en texto seguro para ReportLab.
    También conserva los saltos de línea.
    """

    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return escape(text).replace("\n", "<br/>")


# ============================================================
# ETIQUETAS
# ============================================================

def _status_label(status):
    """
    Convierte el valor interno del estado
    en el texto que verá el cliente.
    """

    labels = {
        "good": "Buen estado",
        "regular": "Regular",
        "bad": "Mal estado",
    }

    return labels.get(status, "No registrado")


def _inventory_type_label(inventory_type):
    """
    Convierte el tipo interno del inventario
    al texto en español.
    """

    labels = {
        "initial": "Inicial",
        "final": "Final",
    }

    return labels.get(
        inventory_type,
        str(inventory_type or "No registrado"),
    )


def _humanize_field_name(field_name):
    """
    Convierte nombres técnicos como:
        cantidad_puertas
    en:
        Cantidad puertas
    """

    return (
        str(field_name)
        .replace("_", " ")
        .strip()
        .capitalize()
    )


# ============================================================
# CAMPOS ADICIONALES
# ============================================================

def _get_extra_field_definitions(
    section,
    item,
    definitions,
):
    """
    Busca la definición original del item para
    poder obtener los nombres de sus campos adicionales.

    También soporta las secciones dinámicas:
        Alcoba auxiliar 2
        Baño auxiliar 3
    """

    base_section_name = section.name

    if section.name.startswith("Alcoba auxiliar "):
        base_section_name = "Alcoba auxiliar"

    elif section.name.startswith("Baño auxiliar "):
        base_section_name = "Baño auxiliar"

    for section_name, section_definitions in definitions.items():

        if base_section_name != section_name:
            continue

        for definition in section_definitions:

            if definition["name"] == item.name:

                return definition.get(
                    "extra_fields",
                    {},
                )

    return {}


# ============================================================
# DESCARGAR IMAGEN DESDE CLOUDINARY
# ============================================================

def _download_image(url):
    """
    Descarga una imagen almacenada en Cloudinary
    usando el certificado CA de certifi.

    Si la imagen falla, el PDF no se rompe:
    simplemente devuelve None.
    """

    if not url:
        return None

    try:

        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        context = ssl.create_default_context(
            cafile=certifi.where()
        )

        with urlopen(
            request,
            context=context,
            timeout=15,
        ) as response:

            return BytesIO(
                response.read()
            )

    except Exception:
        return None


# ============================================================
# CREAR IMAGEN PARA EL PDF
# ============================================================

def _build_image(
    url,
    max_width,
    max_height,
):
    """
    Descarga una imagen y la ajusta
    proporcionalmente al espacio disponible.
    """

    image_data = _download_image(url)

    if image_data is None:

        return Paragraph(
            "No se pudo cargar la imagen.",
            ParagraphStyle(
                "photo_error",
                fontName="Helvetica",
                fontSize=8,
                textColor=colors.HexColor(
                    "#777777"
                ),
                alignment=TA_CENTER,
            ),
        )

    try:

        # Asegurarnos de que el archivo comienza
        # desde el principio.
        image_data.seek(0)

        # Usamos ImageReader solamente para
        # conocer las dimensiones originales.
        image_reader = ImageReader(
            image_data
        )

        original_width, original_height = (
            image_reader.getSize()
        )

        if (
            not original_width
            or not original_height
        ):
            raise ValueError(
                "Dimensiones de imagen invalidas"
            )

        ratio = min(
            max_width / float(
                original_width
            ),
            max_height / float(
                original_height
            ),
        )

        width = original_width * ratio
        height = original_height * ratio

        # Volvemos al comienzo del archivo.
        image_data.seek(0)

        # IMPORTANTE:
        # Pasamos directamente BytesIO a Image,
        # no ImageReader.
        return Image(
            image_data,
            width=width,
            height=height,
            lazy=0,
        )

    except Exception as error:

        print(
            "ERROR AL PROCESAR IMAGEN:",
            error,
        )

        return Paragraph(
            "No se pudo cargar la imagen.",
            ParagraphStyle(
                "photo_error_2",
                fontName="Helvetica",
                fontSize=8,
                textColor=colors.HexColor(
                    "#777777"
                ),
                alignment=TA_CENTER,
            ),
        )


# ============================================================
# GALERIA DE FOTOS
# ============================================================

def _photo_gallery(
    photos,
    caption_style,
    caption_prefix="Foto",
):
    """
    Organiza las fotografías en dos columnas.
    """

    if not photos:
        return []

    photo_cells = []

    cell_width = 3.35 * inch

    max_width = 3.0 * inch
    max_height = 2.15 * inch

    for index, photo in enumerate(
        photos,
        start=1,
    ):

        photo_cells.append(
            [
                _build_image(
                    photo.secure_url,
                    max_width=max_width,
                    max_height=max_height,
                ),

                Spacer(
                    1,
                    6,
                ),

                Paragraph(
                    f"{caption_prefix} {index}",
                    caption_style,
                ),
            ]
        )

    rows = []

    for index in range(
        0,
        len(photo_cells),
        2,
    ):

        row = photo_cells[
            index:index + 2
        ]

        if len(row) == 1:
            row.append("")

        rows.append(row)

    gallery = Table(
        rows,
        colWidths=[
            cell_width,
            cell_width,
        ],
        hAlign="LEFT",
    )

    gallery.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    14,
                ),
            ]
        )
    )

    return [gallery]


# ============================================================
# PIE DE PAGINA
# ============================================================

def _build_watermark(url, opacity=0.05):
    """
    Prepara el logo de la organización como marca de agua
    difuminada (transparente) para dibujarlo en cada página.
    Devuelve None si la organización no tiene logo.
    """

    image_data = _download_image(url)

    if image_data is None:
        return None

    try:
        image_data.seek(0)

        logo = PILImage.open(
            image_data
        ).convert("RGBA")

        alpha = logo.getchannel("A").point(
            lambda value: int(value * opacity)
        )

        logo.putalpha(alpha)

        buffer = BytesIO()
        logo.save(buffer, format="PNG")
        buffer.seek(0)

        return ImageReader(buffer)

    except Exception:
        return None


def _decorate_page(
    canvas,
    doc,
    watermark=None,
    organization_name="",
):
    """
    Dibuja en cada página la marca de agua (detrás del contenido)
    y el pie de página con el nombre de la organización y el número.
    """

    canvas.saveState()

    width, height = letter

    if watermark is not None:

        image_width, image_height = watermark.getSize()

        max_size = 4.8 * inch

        ratio = min(
            max_size / float(image_width),
            max_size / float(image_height),
        )

        draw_width = image_width * ratio
        draw_height = image_height * ratio

        canvas.drawImage(
            watermark,
            (width - draw_width) / 2,
            (height - draw_height) / 2,
            width=draw_width,
            height=draw_height,
            mask="auto",
        )

    canvas.setStrokeColor(
        colors.HexColor("#d9dee4")
    )

    canvas.line(
        doc.leftMargin,
        0.48 * inch,
        width - doc.rightMargin,
        0.48 * inch,
    )

    canvas.setFont(
        "Helvetica",
        8,
    )

    canvas.setFillColor(
        colors.HexColor("#777777")
    )

    canvas.drawString(
        doc.leftMargin,
        0.28 * inch,
        _safe_text(organization_name, default="Habita"),
    )

    canvas.drawRightString(
        width - doc.rightMargin,
        0.28 * inch,
        f"Página {doc.page}",
    )

    canvas.restoreState()


# ============================================================
# GENERAR PDF
# ============================================================

_SECTION_BAR_STYLE = ParagraphStyle(
    "section_bar",
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=16,
    textColor=colors.white,
)

_ITEM_BAR_STYLE = ParagraphStyle(
    "item_bar",
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#1f3a5c"),
)


def _section_header(text):
    """
    Título de sección: barra azul con texto blanco,
    para distinguir cada sección al hacer scroll.
    """

    table = Table(
        [[Paragraph(text, _SECTION_BAR_STYLE)]],
        colWidths=[7.0 * inch],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1f3a5c")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    table.spaceBefore = 16
    table.spaceAfter = 8
    table.keepWithNext = True

    return table


def _item_header(text):
    """
    Título de característica: franja clara con borde azul
    a la izquierda, para diferenciarla del contenido.
    """

    table = Table(
        [[Paragraph(text, _ITEM_BAR_STYLE)]],
        colWidths=[7.0 * inch],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8eef6")),
                ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#2f5d8c")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    table.spaceBefore = 8
    table.spaceAfter = 6
    table.keepWithNext = True

    return table


def build_inventory_pdf(
    inventory,
    definitions,
):
    """
    Construye el PDF completo de un inventario.

    Recibe:
        inventory
        definitions

    Devuelve:
        BytesIO con el PDF listo para descargar.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,

        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,

        topMargin=0.58 * inch,
        bottomMargin=0.68 * inch,

        title=(
            f"Inventario - "
            f"{inventory.property.name}"
        ),

        author=(
            "Plataforma de inventarios"
        ),
    )

    styles = getSampleStyleSheet()

    # ========================================================
    # ESTILOS
    # ========================================================

    title_style = ParagraphStyle(
        "inventory_title",

        parent=styles["Title"],

        fontName="Helvetica-Bold",

        fontSize=21,

        leading=25,

        textColor=colors.HexColor(
            "#1f3a5c"
        ),

        alignment=TA_CENTER,

        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "inventory_subtitle",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=10,

        leading=14,

        textColor=colors.HexColor(
            "#4a4a4a"
        ),

        alignment=TA_CENTER,

        spaceAfter=18,
    )

    section_style = ParagraphStyle(
        "section_title",

        parent=styles["Heading2"],

        fontName="Helvetica-Bold",

        fontSize=14,

        leading=18,

        textColor=colors.HexColor(
            "#1f3a5c"
        ),

        spaceBefore=14,

        spaceAfter=10,
    )

    item_title_style = ParagraphStyle(
        "item_title",

        parent=styles["Heading3"],

        fontName="Helvetica-Bold",

        fontSize=11,

        leading=14,

        textColor=colors.HexColor(
            "#1f3a5c"
        ),

        spaceBefore=5,

        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "body",

        parent=styles["BodyText"],

        fontName="Helvetica",

        fontSize=9.5,

        leading=14,

        textColor=colors.HexColor(
            "#333333"
        ),

        spaceAfter=4,
    )

    small_style = ParagraphStyle(
        "small",

        parent=body_style,

        fontSize=8.5,

        leading=11,
    )

    label_style = ParagraphStyle(
        "label",

        parent=body_style,

        fontName="Helvetica-Bold",

        textColor=colors.HexColor(
            "#1f3a5c"
        ),
    )

    caption_style = ParagraphStyle(
        "caption",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=8,

        leading=10,

        textColor=colors.HexColor(
            "#666666"
        ),

        alignment=TA_CENTER,
    )

    signature_name_style = ParagraphStyle(
        "signature_name",

        parent=body_style,

        fontName="Helvetica-Bold",

        fontSize=11,

        textColor=colors.HexColor(
            "#1f3a5c"
        ),

        alignment=TA_CENTER,
    )

    story = []

    property_obj = inventory.property
    organization = property_obj.organization

    # ========================================================
    # ENCABEZADO
    # ========================================================

    story.append(
        Paragraph(
            "INVENTARIO DE ENTREGA DE INMUEBLE",
            title_style,
        )
    )

    story.append(
        Paragraph(
            (
                f"{_safe_text(property_obj.name)} "
                f"- "
                f"{_inventory_type_label(inventory.inventory_type)}"
            ),
            subtitle_style,
        )
    )

    # ========================================================
    # DATOS GENERALES
    # ========================================================

    property_rows = [
        [
            Paragraph(
                "Propiedad",
                label_style,
            ),

            Paragraph(
                _safe_text(
                    property_obj.name
                ),
                body_style,
            ),
        ],

        [
            Paragraph(
                "Numero de contrato",
                label_style,
            ),

            Paragraph(
                _safe_text(
                    getattr(
                        property_obj,
                        "property_number",
                        "",
                    )
                ),
                body_style,
            ),
        ],

        [
            Paragraph(
                "Tipo de inventario",
                label_style,
            ),

            Paragraph(
                _inventory_type_label(
                    inventory.inventory_type
                ),
                body_style,
            ),
        ],

        [
            Paragraph(
                "Fecha de creacion",
                label_style,
            ),

            Paragraph(
                localtime(
                    inventory.created_at
                ).strftime(
                    "%d/%m/%Y %H:%M"
                ),
                body_style,
            ),
        ],
    ]

    # --------------------------------------------------------
    # Campos adicionales de la propiedad
    # --------------------------------------------------------

    optional_property_fields = [
        (
            "address",
            "Direccion",
        ),

        (
            "tenant_name",
            "Nombres y apellidos del arrendatario",
        ),

        (
            "document_label",
            "Documento",
        ),

        (
            "tenant_email",
            "Correo del arrendatario",
        ),
    ]

    for field_name, label in (
        optional_property_fields
    ):

        value = getattr(
            property_obj,
            field_name,
            "",
        )

        if value:

            property_rows.append(
                [
                    Paragraph(
                        label,
                        label_style,
                    ),

                    Paragraph(
                        _safe_text(value),
                        body_style,
                    ),
                ]
            )

    property_table = Table(
        property_rows,

        colWidths=[
            1.85 * inch,
            5.15 * inch,
        ],

        hAlign="LEFT",
    )

    property_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor(
                        "#f2f2f2"
                    ),
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor(
                        "#d9dee4"
                    ),
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(
        property_table
    )

    story.append(
        Spacer(
            1,
            12,
        )
    )

    # ========================================================
    # SECCIONES DEL INVENTARIO
    # ========================================================

    sections = inventory.sections.all()

    for section in sections:

        # ------------------------------------------------
        # Sección especial: Llaves entregadas
        # ------------------------------------------------

        if section.name == KEYS_SECTION_NAME:

            story.append(
                _section_header(_safe_text(
                        section.name
                    ))
            )

            for item in section.items.all():

                quantity = (
                    item.extra_data or {}
                ).get(
                    "quantity",
                    "",
                )

                if not quantity:
                    quantity = "Sin registrar"

                keys_table = Table(
                    [
                        [
                            Paragraph(
                                "Cantidad de llaves",
                                label_style,
                            ),

                            Paragraph(
                                _safe_text(quantity),
                                body_style,
                            ),
                        ],
                    ],

                    colWidths=[
                        1.85 * inch,
                        5.15 * inch,
                    ],

                    hAlign="LEFT",
                )

                keys_table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (0, -1),
                                colors.HexColor(
                                    "#f2f2f2"
                                ),
                            ),

                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.HexColor(
                                    "#d9dee4"
                                ),
                            ),

                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP",
                            ),

                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                7,
                            ),

                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                7,
                            ),

                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                7,
                            ),

                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                7,
                            ),
                        ]
                    )
                )

                story.append(
                    keys_table
                )

                story.append(
                    Spacer(
                        1,
                        12,
                    )
                )

            continue

        story.append(
            _section_header(_safe_text(
                    section.name
                ))
        )

        for item in section.items.all():

            story.append(
                _item_header(_safe_text(
                        item.name
                    ))
            )

            # ------------------------------------------------
            # ITEM QUE SOLO ES DESCRIPCION
            # ------------------------------------------------

            if item.is_description:

                if item.description:

                    story.append(
                        Paragraph(
                            (
                                "<b>Descripcion:</b> "
                                f"{_safe_text(item.description)}"
                            ),
                            body_style,
                        )
                    )

                else:

                    story.append(
                        Paragraph(
                            "Sin descripcion registrada.",
                            small_style,
                        )
                    )

            # ------------------------------------------------
            # ITEM NORMAL
            # ------------------------------------------------

            else:

                detail_rows = [
                    [
                        Paragraph(
                            "Tipo o material",
                            label_style,
                        ),

                        Paragraph(
                            _safe_text(
                                item.item_type
                            ),
                            body_style,
                        ),
                    ],

                    [
                        Paragraph(
                            "Estado",
                            label_style,
                        ),

                        Paragraph(
                            _status_label(
                                item.status
                            ),
                            body_style,
                        ),
                    ],
                ]

                # --------------------------------------------
                # CAMPOS ADICIONALES
                # --------------------------------------------

                extra_field_definitions = (
                    _get_extra_field_definitions(
                        section,
                        item,
                        definitions,
                    )
                )

                for field_name, value in (
                    (item.extra_data or {}).items()
                ):

                    if not value:
                        continue

                    field_definition = (
                        extra_field_definitions.get(
                            field_name
                        )
                    )

                    if isinstance(
                        field_definition,
                        dict,
                    ):

                        field_label = (
                            field_definition.get(
                                "label",
                                _humanize_field_name(
                                    field_name
                                ),
                            )
                        )

                    elif isinstance(
                        field_definition,
                        str,
                    ):

                        field_label = (
                            field_definition
                        )

                    else:

                        field_label = (
                            _humanize_field_name(
                                field_name
                            )
                        )

                    detail_rows.append(
                        [
                            Paragraph(
                                _safe_text(
                                    field_label
                                ),
                                label_style,
                            ),

                            Paragraph(
                                _safe_text(value),
                                body_style,
                            ),
                        ]
                    )

                # --------------------------------------------
                # DESCRIPCION
                # --------------------------------------------

                if item.description:

                    detail_rows.append(
                        [
                            Paragraph(
                                "Descripcion",
                                label_style,
                            ),

                            Paragraph(
                                _safe_text(
                                    item.description
                                ),
                                body_style,
                            ),
                        ]
                    )

                detail_table = Table(
                    detail_rows,

                    colWidths=[
                        1.85 * inch,
                        5.15 * inch,
                    ],

                    hAlign="LEFT",
                )

                detail_table.setStyle(
                    TableStyle(
                        [
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.4,
                                colors.HexColor(
                                    "#d9dee4"
                                ),
                            ),

                            (
                                "BACKGROUND",
                                (0, 0),
                                (0, -1),
                                colors.HexColor(
                                    "#f8f9fa"
                                ),
                            ),

                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP",
                            ),

                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                6,
                            ),

                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                6,
                            ),

                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),

                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                        ]
                    )
                )

                story.append(
                    detail_table
                )

            # ------------------------------------------------
            # FOTOS DEL ITEM
            # ------------------------------------------------

            photos = list(
                item.photos.all()
            )

            if photos:

                story.append(
                    Spacer(
                        1,
                        8,
                    )
                )

                story.append(
                    Paragraph(
                        "Fotos",
                        label_style,
                    )
                )

                story.extend(
                    _photo_gallery(
                        photos,
                        caption_style,
                    )
                )

            story.append(
                Spacer(
                    1,
                    5,
                )
            )

    signature = getattr(
        inventory,
        "signature",
        None,
    )

    # ========================================================
    # NOTAS Y DECLARACIONES
    # ========================================================

    notes_snapshot = (
        getattr(signature, "notes_snapshot", None)
        if signature
        else None
    )

    if notes_snapshot:

        story.append(
            PageBreak()
        )

        story.append(
            _section_header("NOTAS Y DECLARACIONES")
        )

        for note in notes_snapshot:

            note_title = _safe_text(
                note.get("title", "")
            )

            note_content = _safe_text(
                note.get("content", "")
            )

            if note_title:

                story.append(
                    Paragraph(
                        f"<b>{note_title}</b>",
                        label_style,
                    )
                )

            if note_content:

                story.append(
                    Paragraph(
                        note_content,
                        body_style,
                    )
                )

            story.append(
                Spacer(
                    1,
                    8,
                )
            )

    # ========================================================
    # FIRMA
    # ========================================================

    if signature:

        story.append(
            PageBreak()
        )

        story.append(
            _section_header("FIRMA DEL INVENTARIO")
        )

        story.append(
            Paragraph(
                (
                    "Firmado por: "
                    f"<b>{_safe_text(signature.name)}</b>"
                ),
                signature_name_style,
            )
        )

        signature_document = (
            signature.document_label
            or inventory.property.document_label
        )

        if signature_document:

            story.append(
                Paragraph(
                    (
                        "Documento: "
                        f"<b>{_safe_text(signature_document)}</b>"
                    ),
                    subtitle_style,
                )
            )

        signature_email = (
            signature.email
            or inventory.property.tenant_email
        )

        if signature_email:

            story.append(
                Paragraph(
                    (
                        "Correo: "
                        f"{_safe_text(signature_email)}"
                    ),
                    subtitle_style,
                )
            )

        story.append(
            Paragraph(
                (
                    "Fecha de firma: "
                    f"{localtime(signature.signed_at).strftime('%d/%m/%Y %H:%M')}"
                ),
                subtitle_style,
            )
        )

        signature_image = _build_image(
            signature.secure_url,
            max_width=3.4 * inch,
            max_height=2.0 * inch,
        )

        signature_table = Table(
            [[signature_image]],

            colWidths=[
                7.0 * inch
            ],

            hAlign="CENTER",
        )

        signature_table.setStyle(
            TableStyle(
                [
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),

                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),

                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor(
                            "#d9dee4"
                        ),
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        12,
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        12,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        12,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        12,
                    ),
                ]
            )
        )

        story.append(
            signature_table
        )


        # ----------------------------------------------------
        # FOTOS DE EVIDENCIA
        # ----------------------------------------------------

        signature_photos = list(
            signature.photos.all()
        )

        if signature_photos:

            story.append(
                Spacer(
                    1,
                    18,
                )
            )

            story.append(
                Paragraph(
                    "Fotos de evidencia",
                    label_style,
                )
            )

            story.extend(
                _photo_gallery(
                    signature_photos,
                    caption_style,
                    caption_prefix="Prueba",
                )
            )

    # ========================================================
    # CREAR DOCUMENTO
    # ========================================================

    watermark = (
        _build_watermark(organization.logo_secure_url)
        if organization.logo_secure_url
        else None
    )

    def decorate(canvas, doc):
        _decorate_page(
            canvas,
            doc,
            watermark=watermark,
            organization_name=organization.name,
        )

    document.build(
        story,
        onFirstPage=decorate,
        onLaterPages=decorate,
    )

    buffer.seek(0)

    return buffer