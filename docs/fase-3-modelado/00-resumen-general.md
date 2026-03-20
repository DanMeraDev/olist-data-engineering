# Fase 3 — Modelado y Carga a Base de Datos

**Dataset:** Olist Brazilian E-Commerce (Kaggle)
**Objetivo:** Disenar el esquema relacional en PostgreSQL, cargar los datos limpios y preparar la infraestructura para el dashboard (Fase 4).

> Todos los datos presentados fueron extraidos de los archivos [`sql/schema.sql`](../../sql/schema.sql), [`src/load_to_db.py`](../../src/load_to_db.py) y [`docker-compose.yml`](../../docker-compose.yml). Los conteos corresponden a la ejecucion real del pipeline de carga.

---

## Motor y Entorno

- **Motor:** PostgreSQL 16 (Alpine)
- **Infraestructura:** Docker Compose para reproducibilidad y futura integracion con n8n
- **Puerto:** 5433 (evita conflicto con PostgreSQL local en 5432)

---

## De 9 CSVs a 8 Tablas

El dataset original tiene 9 CSVs. En el modelado se redujo a 8 tablas: `category_translation` fue absorbida por `products` mediante un JOIN durante la carga.

| Tabla | Registros | Origen |
|-------|----------:|--------|
| geolocation | 19,010 | Agregada de 720,257 filas (1 por zip code) |
| customers | 99,441 | Directo |
| sellers | 3,095 | Directo |
| products | 32,951 | JOIN con category_translation |
| orders | 99,441 | Directo |
| order_items | 112,650 | Directo |
| order_payments | 103,883 | Directo |
| order_reviews | 99,224 | Directo |

---

## Archivos Clave

| Archivo | Funcion |
|---------|---------|
| `docker-compose.yml` | Levanta PostgreSQL en Docker |
| `sql/schema.sql` | DDL: tablas, PKs, FKs, indices |
| `src/load_to_db.py` | Carga CSVs limpios a PostgreSQL |
