# Skill: Inventory Management

Gestión de inventarios (inicial/final) en el sistema Inmuebles App.

## Estructura del Inventario

- **Inventory**: Tipo (initial/final), propiedad, fecha
- **InventorySection**: Secciones ordenadas (ej: "Cocina", "Habitación 1")
- **InventoryItem**: Características dentro de secciones
  - `name`: Nombre del ítem
  - `item_type`: Tipo o material
  - `status`: good (Buen estado), regular (Regular), bad (Mal estado)
  - `description`: Descripción adicional
  - `type_options`: JSON con opciones de tipo/material
  - `extra_data`: JSON con datos adicionales
  - `order`: Orden de visualización
- **InventoryItemPhoto**: Fotos de evidencia por ítem
- **InventorySignature**: Firma digital con nombre, fotos de evidencia

## Crear inventario

1. Verificar permisos de admin
2. Obtener propiedad: `get_object_or_404(Property, id=property_id, organization=organization)`
3. Crear `Inventory` con tipo (initial/final)
4. Agregar secciones con orden
5. Agregar ítems a cada sección
6. Subir fotos de ítems a Cloudinary (carpeta: `inventory_items`)
7. Subir fotos de firma a Cloudinary (carpeta: `inventory_signatures`)

## Generar PDF

Usar `inventory/pdf.py` con ReportLab:

```python
from inventory.pdf import generate_inventory_pdf

pdf = generate_inventory_pdf(inventory)
# Retornar como HttpResponse con Content-Type: application/pdf
```

## Flujo de fotos

```python
# Upload de foto de ítem
result = cloudinary.uploader.upload(photo, folder="inventory_items")
InventoryItemPhoto.objects.create(
    item=item,
    public_id=result["public_id"],
    secure_url=result["secure_url"]
)

# Upload de firma
result = cloudinary.uploader.upload(signature_image, folder="inventory_signatures")
InventorySignaturePhoto.objects.create(
    signature=signature,
    public_id=result["public_id"],
    secure_url=result["secure_url"]
)
```

## Estados de ítem

| Valor | Display |
|-------|---------|
| `good` | Buen estado |
| `regular` | Regular |
| `bad` | Mal estado |

## Orden de secciones e ítems

Ambos usan `order` (PositiveIntegerField) para ordenamiento. Por defecto `Meta.ordering = ["order", "id"]`.
