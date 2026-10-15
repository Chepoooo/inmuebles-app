# AGENTS.md - Inmuebles App

Este archivo proporciona orientación a los agentes de IA cuando trabajan en este proyecto.

## Resumen del Proyecto

Sistema de gestión inmobiliaria multi-tenant con Django 6.1 y PostgreSQL. Administra propiedades, inventarios, reparaciones y organizaciones con roles de usuario.

## Comandos Esenciales

```bash
# Desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Tests
python manage.py test

# Shell
python manage.py shell

# Crear superusuario
python manage.py createsuperuser
```

## Convenciones de Código

### General
- **Idioma**: Todo el código, comentarios y documentación en **español**
- **Estilo**: PEP 8 para Python
- **Nombres de variables/functions**: snake_case
- **Nombres de clases**: PascalCase

### Django Específico
- **Vistas**: Basadas en funciones (no CBVs)
- **URLs**: snake_case con nombre descriptivo
- **Templates**: kebab-case (ej: `property_list.html`)
- **Forms**: En `forms.py` de cada app
- **Models**: En `models.py`, con `related_name` descriptivos

### Decoradores Personalizados
```python
from accounts.utils import admin_required, get_current_organization

@login_required
@admin_required
def mi_vista(request):
    organization = get_current_organization(request)
    # ...
```

### Manejo de Organizaciones
- TODAS las consultas deben filtrar por `organization` actual
- Usar `get_current_organization(request)` para obtener la organización de la sesión
- Verificar membresía antes de cualquier operación

### Imágenes (Cloudinary)
```python
import cloudinary.uploader

# Upload
result = cloudinary.uploader.upload(photo, folder="properties")
instance.photo_public_id = result["public_id"]
instance.photo_url = result["secure_url"]

# Delete
cloudinary.uploader.destroy(public_id)
```

### Respuestas HTTP
- Éxito: `return redirect("nombre_url")`
- Error 404: `get_object_or_404(Modelo, id=id, organization=organization)`
- Formulario inválido: re-renderizar template con `form.errors`

## Estructura de Apps

### accounts/
- **models.py**: Vacío (usa User de Django contrib)
- **views.py**: `home`, `organization_select`, `organization_set`
- **utils.py**: `admin_required` (decorador), `get_current_organization`
- **urls.py**: Login, logout, selección de organización

### organizations/
- **models.py**: `Organization`, `Membership` (con roles: admin/viewer/repair_user)
- **views.py**: CRUD de organizations, invitación de usuarios
- **urls.py**: Bajo `/organizations/`

### properties/
- **models.py**: `Property` (con foto Cloudinary)
- **views.py**: `property_list`, `property_detail`, `property_create`, `property_update`, `property_delete`
- **forms.py**: `PropertyForm`
- **urls.py**: Bajo `/properties/`

### inventory/
- **models.py**: `Inventory`, `InventorySection`, `InventoryItem`, `InventoryItemPhoto`, `InventorySignature`, `InventorySignaturePhoto`
- **views.py**: Gestión de inventarios
- **pdf.py**: Generación de PDF con ReportLab
- **templatetags**: Tags personalizados
- **urls.py**: Bajo `/inventory/`

### repairs/
- **models.py**: `Repair`, `RepairPhoto`
- **views.py**: CRUD de reparaciones
- **urls.py**: Bajo `/repairs/`

## Patrones de URL

```python
# Lista
path("", views.property_list, name="property_list")

# Detalle
path("<int:property_id>/", views.property_detail, name="property_detail")

# Crear
path("crear/", views.property_create, name="property_create")

# Editar
path("<int:property_id>/editar/", views.property_update, name="property_update")

# Eliminar
path("<int:property_id>/eliminar/", views.property_delete, name="property_delete")
```

## Flujo de Autenticación

1. Usuario inicia sesión en `/accounts/login/`
2. `home` verifica si tiene organización seleccionada
3. Si no tiene, redirige a `organization_select`
4. Si tiene una sola, selecciona automáticamente
5. Si tiene varias, muestra lista para elegir
6. `organization_set` guarda en sesión y redirige a `property_list`

## Manejo de Errores

- **Organización no encontrada**: Redirigir a `organization_select`
- **Sin permisos**: Retornar 403 o redirigir
- **Objeto no encontrado**: `get_object_or_404`
- **Formulario inválido**: Re-renderizar con errores

## Testing

```bash
# Todos los tests
python manage.py test

# Test específico de una app
python manage.py test properties

# Test específico de una clase
python manage.py test properties.tests.PropertyModelTest

# Con coverage
coverage run manage.py test
coverage report
```

## Variables de Entorno Requeridas

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | Modo debug (True/False) |
| `DB_NAME` | Nombre de la base de datos PostgreSQL |
| `DB_USER` | Usuario de PostgreSQL |
| `DB_PASSWORD` | Contraseña de PostgreSQL |
| `DB_HOST` | Host de PostgreSQL |
| `DB_PORT` | Puerto de PostgreSQL |
| `CLOUDINARY_CLOUD_NAME` | Cloud name de Cloudinary |
| `CLOUDINARY_API_KEY` | API Key de Cloudinary |
| `CLOUDINARY_API_SECRET` | API Secret de Cloudinary |
| `GOOGLE_MAPS_API_KEY` | API Key de Google Maps |

## Consideraciones de Seguridad

- Nunca commitear `.env` al repositorio
- Usar `SECRET_KEY` diferente en producción
- `DEBUG=False` en producción
- Configurar `ALLOWED_HOSTS` apropiadamente
- Validar permisos en cada vista
- Filtrar por organization para prevenir data leakage entre tenants

## Contexto de Negocio

- **Zona horaria**: America/Bogota
- **Moneda**: COP (Peso colombiano)
- **Idioma principal**: Español
- **Tipos de propiedad**: Casa, Apartamento, Aparta estudio, Oficina, Bodega, Local
- **Estados de inventario**: Buen estado, Regular, Mal estado
- **Estados de reparación**: Pendiente, En progreso, Completada
