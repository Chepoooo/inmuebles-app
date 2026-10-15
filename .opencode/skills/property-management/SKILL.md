# Skill: Property Management

Gestión de propiedades en el sistema Inmuebles App.

## Crear una nueva propiedad

1. Verificar que el usuario tenga rol `admin` en la organización actual
2. Obtener la organización actual: `get_current_organization(request)`
3. Crear el formulario `PropertyForm` con los datos del request
4. Si hay foto, subir a Cloudinary en carpeta `properties`
5. Guardar con `organization` asignada
6. Redirigir a `property_detail`

## Campos requeridos

- `name` (max 150)
- `address` (max 255)
- `property_number` (max 100)
- `tenant_name` (max 150)
- `document_number` (max 50)
- `tenant_email` (email válido)
- `property_type`: Casa, Apartamento, Aparta estudio, Oficina, Bodega, Local
- `photo` (opcional, imagen)
- `created_at` (fecha)

## Editar propiedad

1. Verificar permisos de admin
2. Obtener propiedad con `get_object_or_404(Property, id=id, organization=organization)`
3. Si hay nueva foto, eliminar la anterior de Cloudinary primero
4. Guardar cambios

## Eliminar propiedad

1. Verificar permisos de admin
2. Confirmar eliminación (POST requerido)
3. Cloudinary: eliminar foto asociada
4. Eliminar registro

## Buscar propiedades

```python
Property.objects.filter(
    organization=organization
).filter(
    Q(name__icontains=search) |
    Q(property_number__icontains=search) |
    Q(tenant_name__icontains=search) |
    Q(address__icontains=search)
)
```

## Paginación

Usar `Paginator` con 15 elementos por página.
