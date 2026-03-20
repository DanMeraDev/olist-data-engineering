# Geolocation (Geolocalización)

**1,000,163 filas** | 5 columnas | Sin nulos | **261,836 duplicados**

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Únicos |
|---------|------|--------|
| geolocation_zip_code_prefix | int64 | 19,015 |
| geolocation_lat | float64 | 716,685 |
| geolocation_lng | float64 | 717,097 |
| geolocation_city | str | 8,011 |
| geolocation_state | str | 27 |

---

## Problemas Detectados

### 1. Duplicados masivos
261,836 filas duplicadas completas (26% del dataset). Promedio de 52.6 registros por zip code.

### 2. Coordenadas fuera de Brasil
> Rango esperado: Lat -33.75 a 5.27 | Lng -73.99 a -34.79

- **31** latitudes fuera de rango (ej: 41.61, 28.01)
- **37** longitudes fuera de rango (ej: 121.11, 13.82)

### 3. Inconsistencias en nombres de ciudad
8,011 ciudades únicas, pero muchas son la misma con diferente escritura:

| Variante | Ejemplo |
|----------|---------|
| Sin acento | `sao paulo` |
| Con acento | `são paulo` |
| Encoding corrupto | `sa£o paulo` |
| Sin espacios | `sãopaulo` |

- 2,082 ciudades con diacríticos (26%)
- 1 ciudad con encoding corrupto (`£`)

### 4. Ciudades con formato incorrecto
2 ciudades incluyen estado y país en el nombre:
- `"rio de janeiro, rio de janeiro, brasil"`
- `"campo alegre de lourdes, bahia, brasil"`

### 5. Precisión inconsistente en coordenadas
Entre 2 y 15 decimales según el registro.

---

## Decisiones Fase 2

- Normalizar ciudades a minúsculas sin diacríticos
- Estandarizar coordenadas a 6 decimales (~10cm de precisión)
- Extraer solo el nombre antes de la primera coma en ciudades con formato incorrecto
- Eliminar o corregir coordenadas fuera de rango
