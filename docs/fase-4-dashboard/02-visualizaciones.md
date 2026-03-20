# Visualizaciones

> Datos extraidos de [`src/dashboard.py`](../../src/dashboard.py). Todas las visualizaciones usan Plotly Express o Plotly Graph Objects renderizados en Streamlit.

---

## Resumen

El dashboard contiene **15 visualizaciones** distribuidas en 6 secciones:

| Seccion | Tipo | Cantidad |
|---------|------|:--------:|
| Header (KPIs) | `st.metric` | 4 |
| Q1 | Barras + Linea | 2 |
| Q2 | Barras horizontales | 2 |
| Q3 | Metricas + Histograma + Barras | 4 + 1 + 1 |
| Q4 | Metricas + Barras + Pie | 3 + 1 + 1 |
| Q5 | Barras agrupadas + Barras apiladas + Alerta | 2 + 1 |

---

## Header — KPIs

4 metricas en fila usando `st.columns(4)` y `st.metric`:

| Metrica | Query | Formato |
|---------|-------|---------|
| Total Ordenes | `COUNT(DISTINCT order_id)` | Numero con separador de miles |
| Clientes Unicos | `COUNT(DISTINCT customer_id)` | Numero con separador de miles |
| Revenue Total | `SUM(price + freight)` | R$ y US$ |
| Ticket Promedio | `AVG(price + freight)` | R$ y US$ |

---

## Q1 — Volumen por Mes

| # | Tipo | Libreria | Descripcion |
|---|------|----------|-------------|
| 1 | `px.bar` | Plotly Express | Ordenes por mes (color `#636EFA`) |
| 2 | `px.line` | Plotly Express | Revenue por mes con marcadores (color `#00CC96`) |

Layout: 2 columnas. Eje X formateado como `%b %Y`. Datos filtrados a Oct 2016 - Ago 2018.

---

## Q2 — Top 10 Categorias

| # | Tipo | Libreria | Descripcion |
|---|------|----------|-------------|
| 1 | `px.bar` (horizontal) | Plotly Express | Top 10 por revenue total R$ (color `#EF553B`) |
| 2 | `px.bar` (horizontal) | Plotly Express | Top 10 por cantidad de ordenes (color `#AB63FA`) |

Layout: 2 columnas. Datos ordenados ascendentemente para que la barra mas larga quede arriba.

---

## Q3 — Tiempos de Entrega

| # | Tipo | Libreria | Descripcion |
|---|------|----------|-------------|
| 1-4 | `st.metric` | Streamlit | Aprobacion (h), Compra->Carrier (dias), Transito (dias), Total (dias) |
| 5 | `px.histogram` | Plotly Express | Distribucion de dias de entrega (0-60 dias, 60 bins, color `#19D3F3`) con linea vertical roja de promedio |
| 6 | `px.bar` | Plotly Express | Tiempo promedio por estado con escala `RdYlGn_r` (solo estados >100 ordenes) |

Layout: 4 metricas en fila, histograma ancho completo, barras por estado ancho completo.

---

## Q4 — Incidencias

| # | Tipo | Libreria | Descripcion |
|---|------|----------|-------------|
| 1-3 | `st.metric` | Streamlit | % cancelaciones (con delta), % reviews negativas, % entregas tardias (con delta) |
| 4 | `px.bar` | Plotly Express | Distribucion de review scores 1-5 (5 colores: rojo a azul) |
| 5 | `px.pie` | Plotly Express | Distribucion de status de ordenes (paleta `Set2`) |

Layout: 3 metricas en fila, 2 graficos en columnas. Los deltas de metricas usan `delta_color="inverse"` (rojo = mas es peor).

---

## Q5 — Distribucion Geografica

| # | Tipo | Libreria | Descripcion |
|---|------|----------|-------------|
| 1 | `go.Bar` (agrupado) | Plotly Graph Objects | Customers vs Sellers por estado (azul `#636EFA` + rojo `#EF553B`) |
| 2 | `px.bar` (apilado) | Plotly Express | Metodos de pago por estado, top 5 estados: SP, RJ, MG, RS, PR (paleta `Set2`) |
| 3 | `st.warning` | Streamlit | Alerta condicional con lista de estados sin sellers y cantidad de clientes afectados |

Layout: 2 graficos en columnas, alerta debajo.

---

## Paleta de Colores

| Color | Hex | Uso |
|-------|-----|-----|
| Azul | `#636EFA` | Ordenes, customers |
| Verde | `#00CC96` | Revenue (linea) |
| Rojo | `#EF553B` | Categorias revenue, sellers |
| Purpura | `#AB63FA` | Categorias ordenes |
| Cyan | `#19D3F3` | Histograma entregas |
| Set2 | (paleta Plotly) | Pie charts, metodos de pago |
| RdYlGn_r | (escala continua) | Tiempo de entrega por estado |
