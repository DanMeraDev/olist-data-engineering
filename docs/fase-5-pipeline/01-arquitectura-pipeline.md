# Arquitectura del Pipeline

> Datos extraidos de [`src/run_pipeline.py`](../../src/run_pipeline.py), [`src/run_cleaning.py`](../../src/run_cleaning.py), [`src/load_to_db.py`](../../src/load_to_db.py) y [`n8n/olist_workflow.json`](../../n8n/olist_workflow.json).

---

## Diagrama del Flujo

```
run_pipeline.py
      |
      v
[Paso 1] run_cleaning.py
      |  Lee 9 CSVs de data/raw/
      |  Aplica transformaciones
      |  Genera 9 CSVs en data/clean/
      |
      v
[Paso 2] load_to_db.py
      |  Ejecuta schema.sql (DROP + CREATE)
      |  Carga 8 tablas a PostgreSQL
      |
      v
[Paso 3] HTTP POST al webhook de n8n
      |  n8n ejecuta 3 queries a PostgreSQL
      |  Formatea mensaje con nodo Code
      |  Envia reporte a Telegram
      |
      v
[Paso 4] streamlit run src/dashboard.py
         Dashboard interactivo en localhost:8501
         Queda corriendo hasta Ctrl+C
```

---

## Paso 1: Limpieza y Transformacion

**Script:** `src/run_cleaning.py`
**Entrada:** 9 CSVs en `data/raw/`
**Salida:** 9 CSVs en `data/clean/`

El script lee los 9 datasets originales de Kaggle y aplica las funciones de limpieza de `src/cleaning/`:

| Dataset | Funcion de limpieza |
|---------|---------------------|
| customers | `limpiar_customers` |
| geolocation | `limpiar_geolocation` |
| order_items | `limpiar_order_items` |
| payments | `limpiar_payments` |
| reviews | `limpiar_reviews` |
| orders | `limpiar_orders` |
| products | `limpiar_products` |
| sellers | `limpiar_sellers` |
| category_translation | `limpiar_category_translation` |

Transformaciones aplicadas: normalizacion de ciudades, conversion de fechas, eliminacion de duplicados, correccion de typos, entre otras (documentadas en Fase 2).

Las columnas datetime se formatean antes de guardar: `%Y-%m-%d %H:%M` para fecha+hora, `%Y-%m-%d` para solo fecha.

---

## Paso 2: Carga a PostgreSQL

**Script:** `src/load_to_db.py`
**Entrada:** 9 CSVs de `data/clean/`
**Salida:** 8 tablas en PostgreSQL

El script ejecuta las siguientes operaciones:

1. **Ejecuta `schema.sql`** — DROP + CREATE de las 8 tablas con PKs, FKs e indices
2. **Agrega geolocation** — De 720,257 filas a 19,010 (1 fila por zip code, usando mediana de coordenadas y moda de ciudad/estado)
3. **JOIN de products con category_translation** — Absorbe la tabla de traduccion, agregando `category_name_english` directamente a products
4. **Renombra columnas** — Estandariza nombres (ej: `customer_zip_code_prefix` a `zip_code_prefix`)
5. **Parsea fechas** — Convierte columnas de texto a datetime
6. **Carga en orden de foreign keys** — geolocation, customers, sellers, products, orders, order_items, order_payments, order_reviews

Conexion por defecto: `postgresql+psycopg://olist:olist123@localhost:5433/olist`

---

## Paso 3: Reporte a Telegram via n8n

**Trigger:** `run_pipeline.py` envia un HTTP POST al webhook de n8n
**URL:** `http://localhost:5678/webhook/olist-pipeline`
**Payload:** `{"trigger": "pipeline"}`

### Nodos del workflow en secuencia

```
Webhook Trigger
      |
      v
Test DB Connection ──> SELECT COUNT(*) FROM orders
      |
      ├──> Query KPIs (total ordenes, clientes, revenue, ticket promedio)
      ├──> Query Top Categorias (top 5 por revenue)
      └──> Query Metricas (dias entrega, cancelaciones, reviews negativas, entregas tardias)
             |
             v
      Formatear Mensaje (nodo Code — JavaScript)
             |
             v
      Enviar a Telegram (parse_mode: Markdown)
             |
             v
      Responder Webhook (status: ok)
```

### Queries ejecutados

**Query KPIs:**

```sql
SELECT
  COUNT(DISTINCT o.order_id) AS total_ordenes,
  COUNT(DISTINCT c.customer_unique_id) AS total_clientes,
  ROUND(SUM(oi.price + COALESCE(oi.freight_value, 0))::numeric, 2) AS revenue_total,
  ROUND(AVG(oi.price + COALESCE(oi.freight_value, 0))::numeric, 2) AS ticket_promedio
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
```

**Query Top 5 Categorias:**

```sql
SELECT
  p.category_name_english AS categoria,
  ROUND(SUM(oi.price + COALESCE(oi.freight_value, 0))::numeric, 2) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category_name_english
ORDER BY revenue DESC
LIMIT 5
```

**Query Metricas:**

```sql
SELECT
  ROUND(AVG(EXTRACT(DAY FROM (delivered_customer_date::TIMESTAMP
    - purchase_timestamp::TIMESTAMP)))::numeric, 1) AS dias_entrega,
  ROUND(COUNT(*) FILTER (WHERE status = 'canceled')::numeric
    / COUNT(*) * 100, 2) AS pct_canceladas,
  ROUND((SELECT COUNT(*) FROM order_reviews WHERE review_score <= 2)::numeric
    / (SELECT COUNT(*) FROM order_reviews) * 100, 2) AS pct_reviews_negativas,
  ROUND(COUNT(*) FILTER (WHERE delivered_customer_date::TIMESTAMP
    > estimated_delivery_date::DATE)::numeric
    / NULLIF(COUNT(*) FILTER (WHERE delivered_customer_date IS NOT NULL), 0)
    * 100, 2) AS pct_entregas_tardias
FROM orders
```

Los 3 queries se disparan en paralelo desde el nodo Test DB Connection. El nodo Formatear Mensaje espera a que los 3 terminen antes de ejecutarse, ya que necesita los datos de todos para construir el reporte.

---

## Paso 4: Dashboard Streamlit

**Script:** `src/dashboard.py`
**URL:** `http://localhost:8501`

Se lanza en modo headless (`--server.headless true`) como un subproceso. El pipeline queda esperando hasta que el usuario presione `Ctrl+C`, momento en el cual el proceso de Streamlit se termina limpiamente.

---

## Manejo de Errores

| Paso | Comportamiento ante error |
|------|--------------------------|
| Paso 1 (limpieza) | `sys.exit(1)` — pipeline se detiene |
| Paso 2 (carga DB) | `sys.exit(1)` — pipeline se detiene |
| Paso 3 (n8n) | Imprime advertencia pero continua (no bloquea el dashboard) |
| Paso 4 (dashboard) | Se lanza como subproceso, `Ctrl+C` lo termina |

El paso 3 maneja tres escenarios de error:
- **ConnectionError:** n8n no esta corriendo — sugiere ejecutar `docker compose up -d`
- **Status != 200:** n8n respondio con error — muestra el status y la respuesta
- **Excepcion generica:** Cualquier otro error — muestra el mensaje
