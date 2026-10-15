# Skill: Repair Management

Gestión de reparaciones en el sistema Inmuebles App.

## Crear reparación

1. Verificar permisos: admin o repair_user
2. Obtener organización y propiedad
3. Obtener `inventory_item` (opcional, puede ser null)
4. Crear `Repair` con tipo, fecha, descripción
5. Subir fotos a Cloudinary (carpeta: `repairs`)

## Campos del modelo Repair

| Campo | Tipo | Requerido |
|-------|------|-----------|
| `organization` | FK Organization | Sí |
| `property` | FK Property | Sí |
| `inventory_item` | FK InventoryItem | No (nullable) |
| `repair_type` | CharField(150) | Sí |
| `report_date` | DateField | Sí |
| `assigned_worker` | CharField(150) | No |
| `quote` | DecimalField(10,2) | No |
| `description` | TextField | No |
| `status` | CharField(20) | Default: pending |

## Estados de reparación

| Valor | Display |
|-------|---------|
| `pending` | Pendiente |
| `in_progress` | En progreso |
| `completed` | Completada |

## Cambiar estado

```python
repair.status = Repair.Status.IN_PROGRESS  # o COMPLETED
repair.save()
```

## Fotos de evidencia

```python
result = cloudinary.uploader.upload(photo, folder="repairs")
RepairPhoto.objects.create(
    repair=repair,
    public_id=result["public_id"],
    secure_url=result["secure_url"]
)
```

## Consultas comunes

```python
# Reparaciones por propiedad
Repair.objects.filter(property=property).order_by("-created_at")

# Reparaciones por estado
Repair.objects.filter(organization=org, status=Repair.Status.PENDING)

# Reparaciones asignadas a un trabajador
Repair.objects.filter(assigned_worker__icontains=worker_name)

# Reparaciones con cotización pendiente
Repair.objects.filter(quote__isnull=True)
```

## Integración con Inventario

Las reparaciones pueden vincularse a un `InventoryItem` específico para rastrear qué característica del inventario requiere reparación.
