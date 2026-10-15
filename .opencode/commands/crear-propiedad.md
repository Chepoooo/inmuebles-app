# Comando: Crear Propiedad

Guía para crear una nueva propiedad en el sistema.

## Uso

```
/crear-propiedad
```

## Descripción

Flujo completo para agregar una nueva propiedad al sistema con sus datos básicos y foto.

## Pasos

1. **Verificar permisos**: Solo usuarios con rol `admin` pueden crear propiedades
2. **Obtener organización**: `get_current_organization(request)`
3. **Crear formulario**: `PropertyForm(request.POST, request.FILES)`
4. **Validar datos**: `form.is_valid()`
5. **Asignar organización**: `property.organization = organization`
6. **Subir foto** (si aplica):
   ```python
   if photo:
       result = cloudinary.uploader.upload(photo, folder="properties")
       property.photo_public_id = result["public_id"]
       property.photo_url = result["secure_url"]
   ```
7. **Guardar**: `property.save()`
8. **Redirigir**: `redirect("property_detail", property_id=property.id)`

## Campos del formulario

| Campo | Tipo | Validación |
|-------|------|------------|
| `name` | CharField | Requerido, max 150 |
| `address` | CharField | Requerido, max 255 |
| `property_number` | CharField | Requerido, max 100 |
| `tenant_name` | CharField | Requerido, max 150 |
| `document_number` | CharField | Requerido, max 50 |
| `tenant_email` | EmailField | Email válido |
| `property_type` | ChoiceField | Casa, Apartamento, etc. |
| `photo` | ImageFile | Opcional |
| `created_at` | DateField | Fecha válida |

## Errores comunes

- **Organización no encontrada**: Redirigir a `organization_select`
- **Sin permisos**: Mostrar error 403
- **Cloudinary fallido**: Mostrar error, no guardar propiedad
