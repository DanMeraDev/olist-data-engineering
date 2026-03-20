# Orders (Órdenes) — Tabla Central

**99,441 filas** | 8 columnas | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Nulos |
|---------|------|-------|
| order_id | str (32 hex) | 0 |
| customer_id | str (32 hex) | 0 |
| order_status | str | 0 |
| order_purchase_timestamp | str | 0 |
| order_approved_at | str | 160 (0.2%) |
| order_delivered_carrier_date | str | 1,783 (1.8%) |
| order_delivered_customer_date | str | 2,965 (3.0%) |
| order_estimated_delivery_date | str | 0 |

> Todas las fechas vienen como texto en formato `DD/MM/YYYY HH:MM`.

---

## Distribución de Status

```
delivered:   96,478 (97.0%)
shipped:      1,107  (1.1%)
canceled:       625  (0.6%)
unavailable:    609  (0.6%)
invoiced:       314  (0.3%)
processing:     301  (0.3%)
created:          5  (0.0%)
approved:         2  (0.0%)
```

**Rango temporal:** Sep 2016 — Oct 2018

---

## Problemas Detectados

### 1. Fechas como texto
Todas las columnas de fecha son strings en formato `DD/MM/YYYY` — requiere `dayfirst=True`.

### 2. Anomalías en fechas nulas
La mayoría de los nulos en fechas de entrega son esperables (órdenes no completadas), excepto:
- **14 órdenes delivered sin `order_approved_at`**
- **8 órdenes delivered sin `order_delivered_customer_date`**
- **2 órdenes delivered sin `order_delivered_carrier_date`**

### 3. Consistencia temporal verificada
- 0 entregas antes de la compra
- 0 aprobaciones antes de la compra
- `order_estimated_delivery_date` solo registra fecha (hora siempre 00:00)
