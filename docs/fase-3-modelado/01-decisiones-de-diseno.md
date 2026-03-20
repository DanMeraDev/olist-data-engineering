# Decisiones de Diseno

> Datos extraidos de [`sql/schema.sql`](../../sql/schema.sql) y [`src/load_to_db.py`](../../src/load_to_db.py).

Se partio del esquema visual proporcionado por el dataset de Kaggle como referencia inicial, que muestra las relaciones entre las 9 tablas conectadas por `order_id`, `customer_id`, `product_id`, `seller_id` y `zip_code_prefix`.

---

## 1. Geolocation Agregada

**Problema:** La tabla original tiene 720,257 filas con multiples registros por zip code (coordenadas ligeramente distintas, ciudades duplicadas). No funciona como tabla de dimension para JOINs.

**Decision:** Agregar a 1 fila por `zip_code_prefix`:
- Coordenadas: mediana de lat/lng
- Ciudad y estado: moda (valor mas frecuente)

**Resultado:** 720,257 filas -> 19,010 zip codes unicos. `zip_code_prefix` es ahora PK.

---

## 2. Products Absorbe Category Translation

**Problema:** Tener una tabla separada de 73 filas solo para traduccion agrega un JOIN innecesario a cada query de productos.

**Decision:** Hacer el JOIN durante la carga e incluir `category_name_english` directamente en la tabla `products`.

**Resultado:** 9 CSVs -> 8 tablas. La columna `category_name_english` queda como nullable (puede ser NULL si la categoria no tiene traduccion).

---

## 3. Columnas Simplificadas

Se quitaron prefijos redundantes de las columnas ya que el contexto lo da la tabla:

| CSV original | Tabla en PostgreSQL |
|---|---|
| `customer_city` | `city` |
| `customer_state` | `state` |
| `seller_zip_code_prefix` | `zip_code_prefix` |
| `order_status` | `status` |
| `order_purchase_timestamp` | `purchase_timestamp` |
| `review_comment_title` | `comment_title` |
| `review_creation_date` | `creation_date` |
| `product_category_name` | `category_name` |
| `product_weight_g` | `weight_g` |

---

## 4. Primary Keys Compuestas

| Tabla | PK |
|-------|----|
| order_items | `(order_id, order_item_id)` |
| order_payments | `(order_id, payment_sequential)` |
| order_reviews | `(review_id, order_id)` |

`order_reviews` usa PK compuesta porque existen 814 `review_id` duplicados asociados a diferentes ordenes (hallazgo de Fase 1).

---

## 5. Foreign Keys

| Tabla | FK | Referencia |
|-------|-----|-----------|
| orders | `customer_id` | customers(customer_id) |
| order_items | `order_id` | orders(order_id) |
| order_items | `product_id` | products(product_id) |
| order_items | `seller_id` | sellers(seller_id) |
| order_payments | `order_id` | orders(order_id) |
| order_reviews | `order_id` | orders(order_id) |

**FK removidas:** `customers.zip_code_prefix` y `sellers.zip_code_prefix` hacia `geolocation`. Razon: geolocation no contiene todos los zip codes del dataset (19,010 de ~15,000 en customers). La relacion sigue existiendo logicamente para LEFT JOINs, pero no se puede imponer como constraint.

---

## 6. Tipos Nativos de PostgreSQL

| Tipo | Uso |
|------|-----|
| `VARCHAR(32)` | IDs hexadecimales (32 caracteres) |
| `TIMESTAMP` | Fechas con hora (purchase, approved, delivered, etc.) |
| `DATE` | Solo fecha (estimated_delivery_date, creation_date) |
| `DECIMAL(10,2)` | Montos monetarios (price, freight_value, payment_value) |
| `DECIMAL(9,6)` | Coordenadas geograficas |
| `SMALLINT` | Enteros pequenos (order_item_id, review_score, photos_qty) |
| `REAL` | Dimensiones fisicas de productos (peso, largo, alto, ancho) |
| `TEXT` | Comentarios de reviews (longitud variable) |
| `CHECK` | `review_score BETWEEN 1 AND 5` |

---

## 7. Indices

| Indice | Tabla | Columna |
|--------|-------|---------|
| idx_orders_customer | orders | customer_id |
| idx_orders_status | orders | status |
| idx_orders_purchase | orders | purchase_timestamp |
| idx_order_items_product | order_items | product_id |
| idx_order_items_seller | order_items | seller_id |
| idx_customers_state | customers | state |
| idx_sellers_state | sellers | state |
| idx_products_category | products | category_name |
| idx_reviews_score | order_reviews | review_score |

Creados para acelerar las queries mas frecuentes del dashboard: filtros por estado, categoria, fecha de compra y score de reviews.

---

## 8. Orden de Carga

El script `load_to_db.py` carga las tablas respetando dependencias de FK:

```
1. geolocation     (sin dependencias)
2. customers       (sin FK a geolocation)
3. sellers         (sin FK a geolocation)
4. products        (sin dependencias)
5. orders          (FK -> customers)
6. order_items     (FK -> orders, products, sellers)
7. order_payments  (FK -> orders)
8. order_reviews   (FK -> orders)
```
