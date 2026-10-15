# Comando: Generar PDF de Inventario

Genera un PDF del inventario de una propiedad.

## Uso

```
/generar-pdf-inventario <property_id>
```

## Descripción

Genera un PDF con la información completa del inventario (inicial o final) de una propiedad específica, incluyendo secciones, ítems, estados y fotografías.

## Implementación

1. Verificar permisos del usuario
2. Obtener organización actual
3. Obtener propiedad: `get_object_or_404(Property, id=property_id, organization=organization)`
4. Obtener último inventario de la propiedad
5. Generar PDF usando `inventory/pdf.py`
6. Retornar PDF como descarga

## Código sugerido

```python
@login_required
def download_inventory_pdf(request, property_id):
    organization = get_current_organization(request)
    property = get_object_or_404(Property, id=property_id, organization=organization)

    inventory = Inventory.objects.filter(
        property=property
    ).latest("created_at")

    pdf_buffer = generate_inventory_pdf(inventory)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="inventario_{property.name}.pdf"'
    return response
```

## Dependencias

- `reportlab` (ya en requirements.txt)
- `inventory/pdf.py` (función `generate_inventory_pdf`)
