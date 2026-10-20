# Comando: Verificar Sistema

Verifica el estado general del sistema Habita.

## Uso

```
/verificar-sistema
```

## Descripción

Ejecuta verificaciones de salud del sistema: conexiones, configuración, migraciones pendientes, etc.

## Verificaciones

### 1. Conexión a base de datos
```python
from django.db import connection
connection.ensure_connection()
```

### 2. Migraciones pendientes
```bash
python manage.py showmigrations --plan | grep -c "\[ \]"
```

### 3. Variables de entorno requeridas
```python
import os

required_vars = [
    "SECRET_KEY",
    "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT",
    "CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET",
]

for var in required_vars:
    if not os.getenv(var):
        print(f"Falta variable: {var}")
```

### 4. Conexión a Cloudinary
```python
import cloudinary
try:
    cloudinary.api.ping()
except Exception as e:
    print(f"Error Cloudinary: {e}")
```

### 5. Archivos estáticos
```bash
python manage.py collectstatic --dry-run
```

## Resultado esperado

- Base de datos: Conectada
- Migraciones: Al día
- Variables de entorno: Completas
- Cloudinary: Conectado
- Static files: Configurados
