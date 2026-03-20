# Infraestructura

> Datos extraidos de [`docker-compose.yml`](../../docker-compose.yml).

---

## Docker Compose

| Parametro | Valor |
|-----------|-------|
| Imagen | `postgres:16-alpine` |
| Contenedor | `olist_postgres` |
| Base de datos | `olist` |
| Usuario | `olist` |
| Password | `olist123` |
| Puerto host | 5433 |
| Puerto contenedor | 5432 |
| Volumen datos | `pgdata` (persistente) |
| Init script | `sql/schema.sql` montado en `/docker-entrypoint-initdb.d/01-schema.sql` |

El puerto 5433 se usa en el host para evitar conflicto con una instalacion local de PostgreSQL en el puerto 5432.

El `schema.sql` se ejecuta automaticamente en la primera inicializacion del contenedor gracias al mecanismo `docker-entrypoint-initdb.d` de la imagen oficial de PostgreSQL.

---

## Como Levantar

```bash
docker compose up -d
```

Verificar que el contenedor esta corriendo:

```bash
docker ps --filter name=olist_postgres
```

---

## Como Cargar los Datos

Requiere las dependencias de Python:

```bash
pip install pandas sqlalchemy "psycopg[binary]"
```

Ejecutar el script de carga:

```bash
python src/load_to_db.py
```

El script:
1. Ejecuta `schema.sql` (DROP + CREATE de todas las tablas)
2. Carga las 8 tablas en orden de dependencias
3. Verifica conteos de cada tabla

---

## Como Conectarse

Desde cualquier cliente PostgreSQL:

```
Host:     localhost
Puerto:   5433
Database: olist
Usuario:  olist
Password: olist123
```

O mediante connection string:

```
postgresql://olist:olist123@localhost:5433/olist
```

---

## Como Reiniciar desde Cero

Si se necesita recrear la base de datos desde cero (por ejemplo, tras cambiar el schema):

```bash
docker compose down -v
docker compose up -d
python src/load_to_db.py
```

El flag `-v` elimina el volumen de datos, forzando una reinicializacion completa.
