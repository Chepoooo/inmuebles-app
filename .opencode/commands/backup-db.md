# Comando: Backup de Base de Datos

Realiza un backup de la base de datos PostgreSQL.

## Uso

```
/backup-db
```

## Descripción

Crea un dump completo de la base de datos PostgreSQL para respaldo o migración.

## Comando shell

```bash
# Backup
pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME < backup_file.sql
```

## Script Python (alternativa)

```python
import subprocess
from datetime import datetime
from django.conf import settings

def backup_database():
    db = settings.DATABASES["default"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.sql"

    command = [
        "pg_dump",
        "-U", db["USER"],
        "-h", db["HOST"],
        "-p", str(db["PORT"]),
        db["NAME"],
    ]

    with open(filename, "w") as f:
        subprocess.run(command, stdout=f, env={
            "PGPASSWORD": db["PASSWORD"]
        })

    return filename
```

## Notas

- Requiere `pg_dump` instalado en el sistema
- El archivo `.env` debe estar configurado correctamente
- Para producción, considerar backups automáticos programados
