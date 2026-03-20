# Reviews (Reseñas)

**99,224 filas** | 7 columnas | 21% nulos (comentarios opcionales) | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Únicos | Nulos |
|---------|------|--------|-------|
| review_id | str (32 hex) | 98,410 | 0 |
| order_id | str (32 hex) | 98,673 | 0 |
| review_score | int64 | 5 | 0 |
| review_comment_title | str | 4,516 | 87,656 (88.3%) |
| review_comment_message | str | 36,155 | 58,247 (58.7%) |
| review_creation_date | datetime | 636 | 0 |
| review_answer_timestamp | datetime | 88,867 | 0 |

---

## Distribución de Scores

```
Score 5: 57,328 (57.8%)
Score 4: 19,142 (19.3%)
Score 3:  8,179  (8.2%)
Score 1: 11,424 (11.5%)
Score 2:  3,151  (3.2%)
```

Promedio: **4.09** — fuerte sesgo positivo.

---

## Problemas Detectados

### 1. Review IDs duplicados
**814 `review_id`** aparecen asociados a más de una orden (mismo review, diferentes `order_id`).

### 2. Órdenes sin review
768 órdenes sin review:
- 646 delivered (clientes que no respondieron)
- 122 en otros estados (normal)

### 3. Anomalía en fechas
85 reviews con hora `01:00` en vez de `00:00`, todas del `2017-10-15` — causado por cambio de horario de verano.

---

## Observaciones

- 58.7% de reviews sin comentario (solo score)
- 88.3% sin título
- Rango de fechas coherente: 2016-2018

---

## Decisiones Fase 2

- Tratar `review_creation_date` solo como fecha (sin hora)
