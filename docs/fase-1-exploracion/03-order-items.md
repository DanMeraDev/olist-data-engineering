# Order Items (Ítems de Órdenes)

**112,650 filas** | 7 columnas | 1 nulo | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Únicos |
|---------|------|--------|
| order_id | str (32 hex) | 98,666 |
| order_item_id | int64 | 21 |
| product_id | str (32 hex) | 32,951 |
| seller_id | str (32 hex) | 3,095 |
| shipping_limit_date | str | 54,615 |
| price | float64 | 5,968 |
| freight_value | **str** (debería ser float) | 6,998 |

---

## Problemas Detectados

### 1. Freight value corrupto
1 registro donde `freight_value` es un espacio `" "` en vez de un número:

| Campo | Valor |
|-------|-------|
| order_id | `0812eb902a67...` |
| price | R$6,735 (el más alto del dataset) |
| freight_value | `" "` |

### 2. Fechas en 2020 (fuera de rango)
4 registros con `shipping_limit_date` en 2020, todos del mismo vendedor. El dataset cubre 2016-2018.

### 3. Fechas como texto
Formato raw: `DD/MM/YYYY HH:MM` — requiere conversión a datetime.

---

## Estadísticas Clave

| | price (R$) | freight_value (R$) |
|---|---|---|
| Mediana | 74.99 | 16.26 |
| Promedio | 120.65 | 19.99 |
| Máximo | 6,735.00 | 409.68 |

- 383 items con flete = 0 (0.3%) — envío gratuito o retiro en tienda
- **4,124 items donde flete > precio (3.7%)** — normal en e-commerce brasileño por distancias
- Mayoría de órdenes con 1 solo item (mediana = 1)

---

## Decisiones Fase 2

- Convertir `shipping_limit_date` a datetime
- Investigar el registro con freight corrupto (imputar o eliminar)
- Investigar los 4 registros con fecha 2020
