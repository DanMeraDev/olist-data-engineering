# Preguntas y Hallazgos

> Datos extraidos de [`src/dashboard.py`](../../src/dashboard.py). Todos los hallazgos provienen de queries SQL ejecutadas contra la base de datos PostgreSQL cargada en Fase 3.

---

## KPIs del Header

Antes de las preguntas, el dashboard presenta 4 metricas globales calculadas mediante JOIN entre `orders` y `order_items`:

| KPI | Descripcion |
|-----|-------------|
| Total Ordenes | `COUNT(DISTINCT order_id)` |
| Clientes Unicos | `COUNT(DISTINCT customer_id)` |
| Revenue Total | `SUM(price + COALESCE(freight_value, 0))` en R$ y US$ |
| Ticket Promedio | `AVG(price + COALESCE(freight_value, 0))` en R$ y US$ |

---

## Q1: Volumen de transacciones por mes

**Pregunta:** Hay estacionalidad en las ventas?

**Metodologia:** Agrupacion por `DATE_TRUNC('month', purchase_timestamp)` con JOIN a `order_items` para calcular revenue por orden. Se filtraron meses incompletos: Sep 2016 (inicio parcial del dataset) y Sep-Oct 2018 (fin parcial).

**Hallazgo:** Crecimiento sostenido desde Oct 2016 hasta mediados de 2018. Noviembre 2017 muestra un pico significativo correspondiente al Black Friday de Brasil. A partir de mediados de 2018 el volumen se estabiliza.

**Visualizaciones:**
- Grafico de barras: ordenes por mes
- Grafico de linea con marcadores: revenue por mes (R$ / US$)

---

## Q2: Top 10 categorias con mayor valor generado

**Pregunta:** Cuales son las categorias mas rentables?

**Metodologia:** JOIN entre `order_items` y `products`, agrupado por `category_name_english`. Se calculan revenue total (`price + freight`) y cantidad de ordenes distintas. Se muestran las top 10 por revenue en dos graficos separados para evidenciar la diferencia entre valor y volumen.

**Hallazgo:** health_beauty lidera en revenue (R$1.44M / ~US$411k), pero bed_bath_table lidera en cantidad de ordenes (9,417). Esto indica que health_beauty vende productos de mayor valor unitario, mientras que bed_bath_table mueve mas volumen a menor precio.

**Visualizaciones:**
- Barras horizontales: top 10 por revenue total (R$)
- Barras horizontales: top 10 por cantidad de ordenes

---

## Q3: Tiempo promedio entre eventos clave del flujo

**Pregunta:** Cuanto tarda cada etapa del proceso de entrega?

**Metodologia:** Se calculan 4 intervalos usando `EXTRACT` sobre las diferencias entre timestamps de `orders`: aprobacion (horas), compra a carrier (dias), transito (dias) y total (dias). Solo se incluyen ordenes con todos los timestamps completos (`delivered_customer_date`, `approved_at`, `delivered_carrier_date` NOT NULL). El desglose por estado filtra estados con mas de 100 ordenes (`HAVING COUNT(*) > 100`).

**Hallazgo:**
- Aprobacion: se completa en horas
- Despacho a carrier: ~2.7 dias promedio
- Transito (carrier a cliente): ~8.9 dias promedio
- Total entrega: ~12 dias promedio

El cuello de botella esta en el transito, no en la aprobacion ni en el despacho. Los estados del norte y nordeste de Brasil tienen tiempos de entrega significativamente mayores que los del sur/sudeste.

**Visualizaciones:**
- 4 metricas: aprobacion (horas), compra->carrier (dias), transito (dias), total (dias)
- Histograma: distribucion de tiempo de entrega (0-60 dias) con linea vertical de promedio
- Barras por estado: tiempo promedio de entrega con escala de color RdYlGn_r (rojo = mas lento)

---

## Q4: Incidencias y resultados negativos

**Pregunta:** Cual es la tasa real de problemas?

**Metodologia:** Se calculan 3 indicadores independientes:
- Cancelaciones: `COUNT FILTER (WHERE status = 'canceled')` sobre `orders`
- Reviews negativas: porcentaje de scores 1-2 sobre `order_reviews`
- Entregas tardias: `delivered_customer_date > estimated_delivery_date` sobre ordenes entregadas

**Hallazgo:** Las cancelaciones son bajas (0.63%), pero las reviews negativas (~14.7%) y las entregas tardias revelan un problema de satisfaccion mayor. La insatisfaccion real es aproximadamente 10 veces mayor que la tasa de cancelacion. Esto sugiere que muchos clientes insatisfechos no cancelan pero si dejan reviews negativas.

**Visualizaciones:**
- 3 metricas: % cancelaciones, % reviews negativas (1-2), % entregas tardias
- Barras: distribucion de review scores (1-5) con escala de color de rojo a azul
- Pie chart: distribucion de status de ordenes (delivered, shipped, canceled, etc.)

---

## Q5: Distribucion geografica de sellers y customers (pregunta libre)

**Pregunta:** Existen estados que solo consumen pero no venden? Hay oportunidades de expansion?

**Metodologia:** FULL OUTER JOIN entre customers y sellers agrupados por estado. Se calcula ratio customer/seller por estado. Adicionalmente, se analiza la distribucion de metodos de pago para los 5 estados con mas actividad (SP, RJ, MG, RS, PR) mediante JOIN entre `orders`, `customers` y `order_payments`.

**Hallazgo:** Sao Paulo concentra el 60% de los sellers pero solo el 42% de los customers, lo que indica una concentracion desproporcionada de la oferta. Varios estados (AL, TO, AP, RR, entre otros) tienen clientes activos pero cero sellers, lo que significa que todas las compras de esos estados dependen de envios desde otros estados, aumentando costos de flete y tiempos de entrega.

**Visualizaciones:**
- Barras agrupadas: customers vs sellers por estado
- Barras apiladas: metodos de pago por estado (top 5 estados)
- Alerta condicional: lista de estados sin ningun seller y cantidad de clientes afectados
