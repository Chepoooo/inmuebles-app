# Skill: Organization Management

Gestión de organizaciones y membresías en el sistema Inmuebles App.

## Crear organización

1. Verificar que el usuario esté autenticado
2. Crear `Organization` con nombre
3. Si hay logo, subir a Cloudinary (carpeta: `organization_logos`)
4. Crear `Membership` con rol `admin` para el creador

## Roles de membresía

| Rol | Valor | Descripción |
|-----|-------|-------------|
| Admin | `admin` | Acceso completo a la organización |
| Viewer | `viewer` | Solo lectura |
| Repair User | `repair_user` | Acceso a reparaciones asignadas |

## Asignar rol a usuario

```python
Membership.objects.create(
    user=user,
    organization=organization,
    role=Membership.Role.ADMIN  # o VIEWER, REPAIR_USER
)
```

## Verificar rol

```python
from accounts.utils import admin_required

# Decorador para vistas que requieren admin
@login_required
@admin_required
def vista_admin(request):
    ...
```

## Obtener organización actual

```python
from accounts.utils import get_current_organization

organization = get_current_organization(request)
if not organization:
    return redirect("organization_select")
```

## Logo de organización

```python
# Upload
result = cloudinary.uploader.upload(logo, folder="organization_logos")
organization.logo_public_id = result["public_id"]
organization.logo_secure_url = result["secure_url"]

# Delete
cloudinary.uploader.destroy(organization.logo_public_id)
```

## Restricciones

- Un usuario puede pertenecer a múltiples organizaciones
- Un usuario solo tiene un rol por organización (constraint: `unique_user_organization`)
- La organización se guarda en sesión: `request.session["organization_id"]`
- Todas las consultas deben filtrar por `organization` actual

## Flujo de selección

1. Usuario inicia sesión
2. `home` verifica `organization_id` en sesión
3. Si no existe o es inválido, redirige a `organization_select`
4. Si tiene una membresía, selecciona automáticamente
5. Si tiene varias, muestra lista para elegir
6. `organization_set` guarda en sesión y redirige a `property_list`
