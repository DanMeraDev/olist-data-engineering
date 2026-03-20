# Fase 1 — Exploración y Diagnóstico del Dataset Olist

**Dataset:** Olist Brazilian E-Commerce (Kaggle)
**Periodo:** Septiembre 2016 — Octubre 2018
**Objetivo:** Identificar problemas de calidad antes de la limpieza (Fase 2).

> Todos los datos, estadísticas y hallazgos presentados en esta documentación fueron calculados y verificados programáticamente en el notebook [`notebooks/01_exploracion_diagnostico.ipynb`](../notebooks/01_exploracion_diagnostico.ipynb). Nada fue estimado ni asumido manualmente.

---

## Vista Panorámica

| Dataset              |   Filas  | Columnas | % Nulos | Duplicados |
|----------------------|---------:|---------:|--------:|-----------:|
| customers            |   99,441 |        5 |    0.00 |          0 |
| geolocation          |1,000,163 |        5 |    0.00 |    261,836 |
| order_items          |  112,650 |        7 |    0.00 |          0 |
| payments             |  103,886 |        5 |    0.00 |          0 |
| reviews              |   99,224 |        7 |   21.01 |          0 |
| orders               |   99,441 |        8 |    0.62 |          0 |
| products             |   32,951 |        9 |    0.83 |          0 |
| sellers              |    3,095 |        4 |    0.00 |          0 |
| category_translation |       71 |        2 |    0.00 |          0 |

---

## Problemas Críticos Detectados

| Tabla | Problema | Impacto |
|-------|----------|---------|
| geolocation | 261,836 filas duplicadas + 68 coordenadas fuera de Brasil | JOINs inflados, datos geográficos incorrectos |
| geolocation | Encoding corrupto en ciudades ("sa£o paulo") y variantes duplicadas | Agregaciones incorrectas por ciudad |
| order_items | 1 `freight_value` corrupto (espacio en vez de número) | Falla en cálculos de flete |
| order_items | 4 registros con fecha en 2020 (dataset es 2016-2018) | Anomalía temporal |
| reviews | 814 `review_id` duplicados entre órdenes distintas | Conteos inflados de reviews |
| orders | Todas las fechas como texto en formato DD/MM/YYYY | Requiere conversión con `dayfirst=True` |
| products | 610 productos sin categoría ni metadatos (1.9%) | Análisis incompleto por categoría |
| category_translation | 4 typos en inglés + 2 categorías sin traducción | Traducciones incorrectas |

---

## Decisiones de Diseño para Fase 2

1. **Texto:** normalizar ciudades a minúsculas sin diacríticos para facilitar JOINs
2. **Coordenadas:** estandarizar a 6 decimales, corregir/eliminar las fuera de rango
3. **Fechas:** convertir todas a datetime con `dayfirst=True`
4. **Categorías:** etiquetar los 610 sin categoría como `"sin_categoria"`, corregir typos, agregar traducciones faltantes
5. **Pagos:** eliminar 3 registros `not_defined` (órdenes canceladas sin valor)
6. **Freight corrupto:** investigar orden y decidir si imputar o eliminar
