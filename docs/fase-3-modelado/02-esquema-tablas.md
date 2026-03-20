# Esquema de Tablas

> Datos extraidos de [`sql/schema.sql`](../../sql/schema.sql). Conteos de la ejecucion real del pipeline de carga.

---

## geolocation — 19,010 registros

Agregada: 1 fila por zip code (mediana de coordenadas, moda de ciudad/estado).

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| zip_code_prefix | INTEGER | **PK** |
| lat | DECIMAL(9,6) | NOT NULL |
| lng | DECIMAL(9,6) | NOT NULL |
| city | VARCHAR(100) | NOT NULL |
| state | CHAR(2) | NOT NULL |

---

## customers — 99,441 registros

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| customer_id | VARCHAR(32) | **PK** |
| customer_unique_id | VARCHAR(32) | NOT NULL |
| zip_code_prefix | INTEGER | NOT NULL |
| city | VARCHAR(100) | NOT NULL |
| state | CHAR(2) | NOT NULL |

---

## sellers — 3,095 registros

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| seller_id | VARCHAR(32) | **PK** |
| zip_code_prefix | INTEGER | NOT NULL |
| city | VARCHAR(100) | NOT NULL |
| state | CHAR(2) | NOT NULL |

---

## products — 32,951 registros

Incluye traduccion al ingles (JOIN con category_translation durante la carga).

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| product_id | VARCHAR(32) | **PK** |
| category_name | VARCHAR(100) | NOT NULL |
| category_name_english | VARCHAR(100) | nullable |
| name_length | SMALLINT | nullable |
| description_length | INTEGER | nullable |
| photos_qty | SMALLINT | nullable |
| weight_g | REAL | nullable |
| length_cm | REAL | nullable |
| height_cm | REAL | nullable |
| width_cm | REAL | nullable |

---

## orders — 99,441 registros

Tabla central del modelo.

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| order_id | VARCHAR(32) | **PK** |
| customer_id | VARCHAR(32) | NOT NULL, **FK** -> customers |
| status | VARCHAR(20) | NOT NULL |
| purchase_timestamp | TIMESTAMP | NOT NULL |
| approved_at | TIMESTAMP | nullable |
| delivered_carrier_date | TIMESTAMP | nullable |
| delivered_customer_date | TIMESTAMP | nullable |
| estimated_delivery_date | DATE | NOT NULL |

---

## order_items — 112,650 registros

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| order_id | VARCHAR(32) | **PK**, **FK** -> orders |
| order_item_id | SMALLINT | **PK** |
| product_id | VARCHAR(32) | NOT NULL, **FK** -> products |
| seller_id | VARCHAR(32) | NOT NULL, **FK** -> sellers |
| shipping_limit_date | TIMESTAMP | NOT NULL |
| price | DECIMAL(10,2) | NOT NULL |
| freight_value | DECIMAL(10,2) | nullable |

---

## order_payments — 103,883 registros

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| order_id | VARCHAR(32) | **PK**, **FK** -> orders |
| payment_sequential | SMALLINT | **PK** |
| payment_type | VARCHAR(20) | NOT NULL |
| payment_installments | SMALLINT | NOT NULL |
| payment_value | DECIMAL(10,2) | NOT NULL |

---

## order_reviews — 99,224 registros

| Columna | Tipo | Restriccion |
|---------|------|-------------|
| review_id | VARCHAR(32) | **PK** |
| order_id | VARCHAR(32) | **PK**, **FK** -> orders |
| review_score | SMALLINT | NOT NULL, CHECK (1-5) |
| comment_title | TEXT | nullable |
| comment_message | TEXT | nullable |
| creation_date | DATE | NOT NULL |
| answer_timestamp | TIMESTAMP | nullable |

---

## Relaciones

```
geolocation (zip_code_prefix)
    <- customers.zip_code_prefix  (logica, sin FK)
    <- sellers.zip_code_prefix    (logica, sin FK)

customers (customer_id)
    <- orders.customer_id         (FK)

orders (order_id)
    <- order_items.order_id       (FK)
    <- order_payments.order_id    (FK)
    <- order_reviews.order_id     (FK)

products (product_id)
    <- order_items.product_id     (FK)

sellers (seller_id)
    <- order_items.seller_id      (FK)
```
