# Limpieza por Dataset

> Datos obtenidos del analisis en [`02-limpieza_y_transformacion.ipynb`](../../notebooks/02-limpieza_y_transformacion.ipynb).

---

## Customers

| Transformacion | Justificacion |
|----------------|---------------|
| Normalizar ciudades | Consistencia con las demas tablas para facilitar JOINs |
| Estados a mayusculas | Estandarizacion (SP, RJ, MG) |

**Resultado:** 99,441 -> 99,441 filas. 0 eliminadas.

---

## Geolocation

| Transformacion | Justificacion |
|----------------|---------------|
| Eliminar 261,836 duplicados | Filas completamente identicas que no aportan informacion |
| Normalizar ciudades | Corregir encoding corrupto, diacriticos y formatos incorrectos |
| Estados a mayusculas | Estandarizacion |
| Eliminar 33 coordenadas fuera de Brasil | Latitudes/longitudes apuntando a otros paises |
| Redondear coordenadas a 6 decimales | Estandarizar precision (~10cm), suficiente para geolocalizacion |
| Eliminar duplicados post-normalizacion | Tras normalizar ciudades y redondear coordenadas, surgen nuevos duplicados |

**Resultado:** 1,000,163 -> 720,257 filas. 279,906 eliminadas (27.99%).

---

## Order Items

| Transformacion | Justificacion |
|----------------|---------------|
| Convertir `freight_value` a numerico | 1 valor no numerico (espacio `" "`, registro con precio maximo R$6,735) -> NaN |
| Convertir `shipping_limit_date` a datetime | Estaba como texto en formato DD/MM/YYYY HH:MM |
| Documentar 4 fechas en 2020 | Se mantienen: son order_items validos, solo la fecha de shipping es anomala |

**Resultado:** 112,650 -> 112,650 filas. 0 eliminadas. 1 freight_value -> NaN.

---

## Payments

| Transformacion | Justificacion |
|----------------|---------------|
| Eliminar 3 pagos `not_defined` | Ordenes canceladas con valor $0, confirmado cruzando con tabla orders |
| Corregir 2 `installments=0` en credit_card | Una tarjeta de credito debe tener minimo 1 cuota |

**Resultado:** 103,886 -> 103,883 filas. 3 eliminadas.

---

## Reviews

| Transformacion | Justificacion |
|----------------|---------------|
| Convertir fechas con `dayfirst=True` | Formato raw DD/MM/YYYY |
| Normalizar `review_creation_date` a solo fecha | 99.9% tiene hora 00:00, las 85 excepciones son por horario de verano |
| Limpiar espacios en comentarios | Espacios en blanco al inicio/final de titulos y mensajes |
| Remover saltos de linea en comentarios | `\n` y `\r` reemplazados por espacio para evitar problemas en CSV |
| Mantener 814 `review_id` duplicados | Son reviews validos del mismo cliente para diferentes ordenes |

**Resultado:** 99,224 -> 99,224 filas. 0 eliminadas.

---

## Orders

| Transformacion | Justificacion |
|----------------|---------------|
| Convertir 5 columnas de fecha con `dayfirst=True` | Critico: sin esto se pierden 60% de las fechas |
| Normalizar `estimated_delivery_date` a solo fecha | Solo registra fecha, hora siempre 00:00 |
| Normalizar `order_status` a minusculas | Consistencia |
| Verificacion temporal | 0 entregas antes de compra confirmado |

**Resultado:** 99,441 -> 99,441 filas. 0 eliminadas.

---

## Products

| Transformacion | Justificacion |
|----------------|---------------|
| Corregir typo `"lenght"` -> `"length"` | Error ortografico en el dataset original (2 columnas afectadas) |
| Etiquetar 610 productos como `"sin_categoria"` | Mejor que dejar NaN para analisis y agrupaciones |
| Convertir 4 productos con peso=0g a NaN | Ningun producto fisico pesa 0 gramos, es dato faltante |

**Resultado:** 32,951 -> 32,951 filas. 0 eliminadas. 610 NaN reemplazados, 4 pesos corregidos.

---

## Sellers

| Transformacion | Justificacion |
|----------------|---------------|
| Normalizar ciudades | Consistencia con las demas tablas. Incluye corregir "lages - sc" -> "lages" |
| Estados a mayusculas | Estandarizacion |

**Resultado:** 3,095 -> 3,095 filas. 0 eliminadas.

---

## Category Translation

| Transformacion | Justificacion |
|----------------|---------------|
| Corregir 4 typos en ingles | `fashio` -> `fashion`, `costruction` -> `construction`, `confort` -> `comfort` |
| Agregar 2 categorias faltantes | `pc_gamer` y `portateis_cozinha_e_preparadores_de_alimentos` existian en products pero no tenian traduccion |

**Resultado:** 71 -> 73 filas. 2 agregadas, 4 valores corregidos.
