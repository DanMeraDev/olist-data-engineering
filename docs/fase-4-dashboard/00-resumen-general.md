# Fase 4 — Dashboard

**Dataset:** Olist Brazilian E-Commerce (Kaggle)
**Objetivo:** Responder 5 preguntas de negocio mediante visualizaciones interactivas, consumiendo datos directamente desde PostgreSQL.

> Todos los datos presentados fueron extraidos de [`src/dashboard.py`](../../src/dashboard.py). Los hallazgos corresponden a la ejecucion real del dashboard contra la base de datos cargada en Fase 3.

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| Framework | Streamlit |
| Graficos | Plotly Express + Plotly Graph Objects |
| Conexion a DB | SQLAlchemy (`pd.read_sql`) |
| Base de datos | PostgreSQL 16 en Docker (puerto 5433) |
| Cache | `@st.cache_resource` para engine, `@st.cache_data(ttl=600)` para queries |

---

## Moneda

Los montos se muestran en Real brasileno (R$) y en Dolar estadounidense (US$), usando una tasa de conversion fija de R$3.50 = US$1 (promedio del periodo 2016-2018).

---

## Preguntas Respondidas

| # | Pregunta |
|---|----------|
| Q1 | Volumen de transacciones por mes — Hay estacionalidad en las ventas? |
| Q2 | Top 10 categorias con mayor valor generado |
| Q3 | Tiempo promedio entre eventos clave del flujo de entrega |
| Q4 | Incidencias y resultados negativos |
| Q5 | Distribucion geografica de sellers y customers (pregunta libre) |

---

## Archivos Clave

| Archivo | Funcion |
|---------|---------|
| `src/dashboard.py` | Dashboard completo (Streamlit + Plotly) |
| `docker-compose.yml` | PostgreSQL en Docker (requerido para ejecutar) |
