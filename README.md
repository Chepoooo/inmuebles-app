# Habita

Sistema de gestión inmobiliaria multi-tenant construido con Django y PostgreSQL.

## Descripción

Aplicación web para administrar propiedades, inventarios (inicial/final), reparaciones y organizaciones con control de acceso basado en roles.

## Requisitos

- Python 3.10+
- PostgreSQL 14+
- Cuenta de Cloudinary (para imágenes)
- Google Maps API Key (opcional)

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd "inmuebles app/APP"

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-secret-key
DEBUG=True
DB_NAME=inmuebles_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
GOOGLE_MAPS_API_KEY=tu_api_key
```

## Estructura del Proyecto

```
APP/
├── accounts/          # Autenticación y gestión de usuarios
├── config/            # Configuración principal de Django
├── inventory/         # Inventarios (inicial/final)
├── organizations/     # Organizaciones y membresías
├── properties/        # CRUD de propiedades
├── repairs/           # Gestión de reparaciones
├── static/            # Archivos estáticos (CSS, JS)
├── templates/         # Plantillas HTML
├── manage.py
├── requirements.txt
└── .env.example
```

## Funcionalidades

### Organizaciones
- Múltiples organizaciones por usuario
- Roles: Admin, Viewer, Repair User
- Logo de organización con Cloudinary

### Propiedades
- CRUD completo de propiedades
- Tipos: Casa, Apartamento, Aparta estudio, Oficina, Bodega, Local
- Datos del arrendatario: nombres y apellidos, tipo de documento (CC, CE, NIT, PPT, Pasaporte), número de documento y correo
- Fotos de propiedades
- Búsqueda por nombre, número, arrendatario o dirección

### Firmas de inventario
- Firma digital del arrendatario con foto y hasta 5 fotos de evidencia
- Los datos de la firma se autocompletan desde la propiedad (nombre, documento, correo) y son editables
- **Notas y declaraciones personalizadas**: biblioteca de notas por organización, seleccionables al firmar y mostradas en el PDF justo encima de la firma

### Inventarios
- Inventarios inicial y final
- Secciones personalizables
- Ítems con: nombre, tipo/material, estado, descripción, fotos
- Firmas digitales con fotos de evidencia
- Generación de PDF (ReportLab)

### Reparaciones
- Estados: Pendiente, En progreso, Completada
- Cotización
- Fotos de evidencia
- Asignación de trabajador

## Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **Admin** | Acceso completo: CRUD de propiedades, inventarios, reparaciones |
| **Viewer** | Solo lectura: ver propiedades, inventarios, reparaciones |
| **Repair User** | Acceso a reparaciones asignadas |

## Convenciones de Código

- Código en español (nombres de campos, mensajes, plantillas)
- Vistas basadas en funciones
- Decoradores: `@login_required`, `@admin_required`
- Validaciones en formularios
- Uploads de imágenes vía Cloudinary
- Paginación: 15 elementos por página

## Testing

```bash
python manage.py test
```

## Despliegue

Para producción:
1. Configurar `DEBUG=False`
2. Configurar `ALLOWED_HOSTS` con el dominio
3. Configurar variables de entorno seguras
4. Usar Gunicorn + Nginx (recomendado)

## Licencia

[Definir licencia]
