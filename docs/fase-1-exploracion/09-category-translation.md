# Category Translation (Traducción de Categorías)

**71 filas** | 2 columnas | Sin nulos | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo |
|---------|------|
| product_category_name | str |
| product_category_name_english | str |

---

## Problemas Detectados

### 1. Typos en traducciones al inglés

| Actual | Correcto |
|--------|----------|
| `fashio_female_clothing` | `fashion_female_clothing` |
| `costruction_tools_garden` | `construction_tools_garden` |
| `costruction_tools_tools` | `construction_tools_tools` |
| `home_confort` | `home_comfort` |

### 2. Categorías faltantes

2 categorías que existen en `products` pero no tienen traducción:
- `pc_gamer`
- `portateis_cozinha_e_preparadores_de_alimentos`

---

## Decisiones Fase 2

- Corregir los 4 typos
- Agregar las 2 traducciones faltantes
