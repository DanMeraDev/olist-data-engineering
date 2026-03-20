# Verificacion Post-Limpieza

> Datos obtenidos del analisis en [`02-limpieza_y_transformacion.ipynb`](../../notebooks/02-limpieza_y_transformacion.ipynb).

Se cargaron los CSVs limpios desde `data/clean/` y se verifico que cada transformacion se aplico correctamente.

---

## Normalizacion de Ciudades

| Tabla | Resultado |
|-------|-----------|
| customers | Ciudades normalizadas correctamente |
| sellers | Ciudades normalizadas correctamente |
| geolocation | Ciudades normalizadas correctamente |

Sin diacriticos, sin encoding corrupto, sin formatos incorrectos en ninguna de las 3 tablas.

---

## Formato de Fechas

| Columna | Nulos | % |
|---------|------:|--:|
| orders.order_purchase_timestamp | 0 | 0.0% |
| orders.order_approved_at | 160 | 0.2% |
| orders.order_delivered_carrier_date | 1,783 | 1.8% |
| orders.order_delivered_customer_date | 2,965 | 3.0% |
| orders.order_estimated_delivery_date | 0 | 0.0% |

Todos los nulos son esperables (ordenes no completadas). `review_creation_date` verificado como solo fecha.

---

## Payments

| Verificacion | Resultado | Esperado |
|-------------|-----------|----------|
| Pagos `not_defined` | 0 | 0 |
| Credit cards con `installments=0` | 0 | 0 |

---

## Products

| Verificacion | Resultado | Esperado |
|-------------|-----------|----------|
| Typo `"lenght"` en columnas | Corregido | `product_name_length`, `product_description_length` |
| Productos `"sin_categoria"` | 610 | 610 |
| Categorias nulas | 0 | 0 |

---

## Geolocation

| Verificacion | Resultado | Esperado |
|-------------|-----------|----------|
| Duplicados restantes | 0 | 0 |
| Coordenadas fuera de Brasil (lat) | 0 | 0 |
| Coordenadas fuera de Brasil (lng) | 0 | 0 |
| Max decimales en coordenadas | 6 | <=6 |

---

## Category Translation

| Verificacion | Resultado |
|-------------|-----------|
| Total categorias | 73 (71 originales + 2 nuevas) |
| `fashion_female_clothing` | Encontrado (antes: `fashio`) |
| `construction_tools_garden` | Encontrado (antes: `costruction`) |
| `construction_tools_tools` | Encontrado (antes: `costruction`) |
| `home_comfort` | Encontrado (antes: `confort`) |
| `pc_gamer` | Encontrado (nueva) |
| `portateis_cozinha_e_preparadores_de_alimentos` | Encontrado (nueva) |

---

Todas las verificaciones pasaron. Los datasets limpios estan en `data/clean/`.
