# Sellers (Vendedores)

**3,095 filas** | 4 columnas | Sin nulos | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Únicos |
|---------|------|--------|
| seller_id | str (32 hex) | 3,095 |
| seller_zip_code_prefix | int64 | 2,246 |
| seller_city | str | 611 |
| seller_state | str | 23 |

---

## Observaciones

**Dataset limpio** — sin problemas de encoding, diacríticos ni normalización.

**Concentración geográfica — Top 5 estados:**

```
SP: 1,849 (59.7%)
PR:   349 (11.3%)
MG:   244  (7.9%)
SC:   190  (6.1%)
RJ:   171  (5.5%)
```

> 59.7% de vendedores en São Paulo (vs 42% de clientes) — mayor concentración de oferta que de demanda.
