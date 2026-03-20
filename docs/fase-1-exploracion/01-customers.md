# Customers (Clientes)

**99,441 filas** | 5 columnas | Sin nulos | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Únicos |
|---------|------|--------|
| customer_id | str (32 hex) | 99,441 |
| customer_unique_id | str (32 hex) | 96,096 |
| customer_zip_code_prefix | int64 | 14,994 |
| customer_city | str | 4,119 |
| customer_state | str | 27 |

---

## Hallazgos Relevantes

**3,345 clientes repiten compra** (diferencia entre `customer_id` y `customer_unique_id`).

**Distribución geográfica — Top 5 estados:**

```
SP: 41,746 (42.0%)
RJ: 12,852 (12.9%)
MG: 11,635 (11.7%)
RS:  5,466  (5.5%)
PR:  5,045  (5.1%)
```

**Ciudades sin normalizar:**
- Todo en minúsculas, sin tildes (ej: "sao paulo" en vez de "são paulo")
- *Decisión:* mantener así para facilitar JOINs entre tablas
