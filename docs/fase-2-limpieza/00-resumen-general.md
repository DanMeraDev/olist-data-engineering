# Fase 2 — Limpieza y Transformacion

**Dataset:** Olist Brazilian E-Commerce (Kaggle)
**Objetivo:** Aplicar transformaciones para obtener datasets limpios y consistentes, justificando cada decision tecnica.

> Todos los datos, estadisticas y resultados presentados en esta documentacion fueron calculados y verificados programaticamente en el notebook [`notebooks/02-limpieza_y_transformacion.ipynb`](../../notebooks/02-limpieza_y_transformacion.ipynb) y ejecutados mediante el pipeline modular en `src/cleaning/`. Nada fue estimado ni asumido manualmente.

---

## Estrategia Modular

Se creo un modulo de limpieza en `src/cleaning/` con un archivo por cada CSV y funciones comunes en `utils.py`. La ejecucion se orquesta desde `src/run_cleaning.py`.

```
src/
├── cleaning/
│   ├── utils.py                    <- funciones comunes
│   ├── clean_customers.py
│   ├── clean_geolocation.py
│   ├── clean_order_items.py
│   ├── clean_payments.py
│   ├── clean_reviews.py
│   ├── clean_orders.py
│   ├── clean_products.py
│   ├── clean_sellers.py
│   └── clean_category_translation.py
└── run_cleaning.py                 <- orquestador
```

---

## Decisiones Globales

1. **Normalizacion de ciudades** — Todas las ciudades a minusculas, sin diacriticos, sin encoding corrupto, extrayendo solo el nombre. Aplica a customers, geolocation y sellers.
2. **Conversion de fechas con `dayfirst=True`** — El formato raw es DD/MM/YYYY (estandar brasileno). Sin este parametro se pierden 60% de las fechas o se interpretan incorrectamente.

---

## Resumen Comparativo Raw vs Clean

| Dataset | Filas raw | Filas clean | Diferencia |
|---------|----------:|------------:|-----------:|
| customers | 99,441 | 99,441 | 0 |
| geolocation | 1,000,163 | 720,257 | -279,906 |
| order_items | 112,650 | 112,650 | 0 |
| payments | 103,886 | 103,883 | -3 |
| reviews | 99,224 | 99,224 | 0 |
| orders | 99,441 | 99,441 | 0 |
| products | 32,951 | 32,951 | 0 |
| sellers | 3,095 | 3,095 | 0 |
| category_translation | 71 | 73 | +2 |
