# Reporte de Telegram

> Datos extraidos del nodo "Formatear Mensaje" en [`n8n/olist_workflow.json`](../../n8n/olist_workflow.json).

---

## Estructura del Reporte

El nodo Code de n8n construye un mensaje en formato Markdown que se envia a Telegram. El mensaje tiene 5 secciones:

---

## 1. KPIs Generales

Datos del query `Query KPIs` (JOIN entre orders, customers y order_items):

| Metrica | Query |
|---------|-------|
| Total Ordenes | `COUNT(DISTINCT o.order_id)` |
| Clientes Unicos | `COUNT(DISTINCT c.customer_unique_id)` |
| Revenue Total | `SUM(oi.price + COALESCE(oi.freight_value, 0))` |
| Ticket Promedio | `AVG(oi.price + COALESCE(oi.freight_value, 0))` |

Los montos se formatean en Reales brasilenos (R$) con `toLocaleString('pt-BR')`.

---

## 2. Top 5 Categorias por Revenue

Datos del query `Query Top Categorias` (JOIN entre order_items y products):

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

Se listan las 5 categorias con mayor revenue, numeradas del 1 al 5, cada una con su revenue en R$.

---

## 3. Logistica

Datos del query `Query Metricas`:

| Metrica | Calculo |
|---------|---------|
| Tiempo promedio de entrega | `AVG(delivered_customer_date - purchase_timestamp)` en dias |
| Entregas tardias | `% donde delivered_customer_date > estimated_delivery_date` |

---

## 4. Incidencias

Datos del mismo query `Query Metricas`:

| Metrica | Calculo |
|---------|---------|
| Cancelaciones | `% de ordenes con status = 'canceled'` |
| Reviews negativas (1-2) | `% de reviews con score <= 2` |

---

## 5. Pie del Mensaje

El reporte cierra con una linea indicando que fue generado automaticamente por el pipeline Olist.

---

## Formato del Mensaje

El mensaje se envia con `parse_mode: Markdown` y usa la siguiente estructura:

```
OLIST E-COMMERCE — REPORTE
━━━━━━━━━━━━━━━━━━━━━━

KPIs Generales
   Total Ordenes: X
   Clientes Unicos: X
   Revenue Total: R$ X
   Ticket Promedio: R$ X

Top 5 Categorias por Revenue
   1. categoria: R$ X
   2. categoria: R$ X
   3. categoria: R$ X
   4. categoria: R$ X
   5. categoria: R$ X

Logistica
   Tiempo promedio de entrega: X dias
   Entregas tardias: X%

Incidencias
   Cancelaciones: X%
   Reviews negativas (1-2): X%

━━━━━━━━━━━━━━━━━━━━━━
Generado automaticamente por el pipeline Olist
```

---

## Consideraciones Tecnicas

- El nodo Code usa JavaScript para acceder a los resultados de los 3 queries via `$('Query KPIs').first().json`, `$('Query Top Categorias').all()` y `$('Query Metricas').first().json`
- El modo de ejecucion es `runOnceForAllItems` — el codigo corre una sola vez con todos los datos disponibles
- Los montos se formatean con `toLocaleString('pt-BR', {minimumFractionDigits: 2})` para usar el formato brasileno (punto como separador de miles, coma para decimales)
- El `chatId` y las credenciales de Telegram se configuran directamente en el nodo (ver [02-configuracion-n8n.md](./02-configuracion-n8n.md))
