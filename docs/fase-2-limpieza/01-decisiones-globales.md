# Decisiones Globales

> Datos obtenidos del analisis en [`02-limpieza_y_transformacion.ipynb`](../../notebooks/02-limpieza_y_transformacion.ipynb).

Estas decisiones aplican a multiples datasets y se implementaron como funciones reutilizables en `src/cleaning/utils.py`.

---

## 1. Normalizacion de Ciudades

**Problema:** Los nombres de ciudades presentan inconsistencias entre tablas (geolocation, customers, sellers):

| Tipo de inconsistencia | Ejemplo |
|------------------------|---------|
| Con/sin diacriticos | "sao paulo" vs "sao paulo" |
| Encoding corrupto | "sa£o paulo" |
| Espacios faltantes | "saopaulo" |
| Formato ciudad, estado, pais | "rio de janeiro, rio de janeiro, brasil" |
| Formato ciudad - estado | "lages - sc" |
| Parentesis | "cidade (info extra)" |

**Decision:** Normalizar todas las ciudades con la funcion `normalizar_ciudad()`:
1. Minusculas
2. Reemplazar `£` por `a` (encoding corrupto)
3. Extraer solo ciudad antes de la primera coma
4. Extraer solo ciudad antes de ` - `
5. Remover parentesis y su contenido
6. Remover diacriticos
7. Colapsar espacios multiples

**Justificacion:** Facilita JOINs entre tablas y evita duplicados falsos. Al ser datos brasilenios donde los diacriticos son inconsistentes incluso en datos oficiales, estandarizar sin diacriticos es la opcion mas robusta.

**Aplica a:** customers, geolocation, sellers.

---

## 2. Conversion de Fechas con `dayfirst=True`

**Problema:** Las fechas en los CSVs raw estan en formato DD/MM/YYYY (estandar brasileno). Pandas por defecto asume MM/DD/YYYY, lo que genera:
- **60% de nulos falsos** — fechas con dia > 12 no se pueden interpretar como mes
- **Fechas incorrectas silenciosas** — ej: `02/10/2017` se interpreta como 10 de febrero en lugar de 2 de octubre

**Decision:** Usar `dayfirst=True` en todas las conversiones via la funcion `convertir_fechas()`.

**Justificacion:** El dataset es brasileno y usa formato DD/MM/YYYY. Sin este parametro se pierden mas de la mitad de las fechas o se interpretan incorrectamente.

**Aplica a:** orders (5 columnas de fecha), reviews (2 columnas), order_items (1 columna).
