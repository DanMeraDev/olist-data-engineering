# Products (Productos)

**32,951 filas** | 9 columnas | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Nulos |
|---------|------|-------|
| product_id | str (32 hex) | 0 |
| product_category_name | str | 610 (1.9%) |
| product_name_lenght* | float64 | 610 |
| product_description_lenght* | float64 | 610 |
| product_photos_qty | float64 | 610 |
| product_weight_g | float64 | 2 |
| product_length_cm | float64 | 2 |
| product_height_cm | float64 | 2 |
| product_width_cm | float64 | 2 |

> *Typo en el dataset original: "lenght" en lugar de "length".

---

## Problemas Detectados

### 1. Productos sin metadatos
**610 productos (1.9%)** sin categoría, nombre, descripción ni fotos — todos los nulos coinciden en las mismas filas.

### 2. Dimensiones sospechosas
- 2 productos sin ninguna dimensión física
- **4 productos con peso = 0g**

### 3. Categorías sin traducción
2 categorías en `products` que no existen en la tabla de traducción:
- `pc_gamer`
- `portateis_cozinha_e_preparadores_de_alimentos`

---

## Top 5 Categorías

```
cama_mesa_banho:        3,029 (9.2%)
esporte_lazer:          2,867 (8.7%)
moveis_decoracao:       2,657 (8.1%)
beleza_saude:           2,444 (7.4%)
utilidades_domesticas:  2,335 (7.1%)
```

---

## Decisiones Fase 2

- Etiquetar los 610 sin categoría como `"sin_categoria"`
- Agregar las 2 traducciones faltantes
