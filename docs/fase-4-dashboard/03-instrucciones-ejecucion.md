# Instrucciones de Ejecucion

> Datos extraidos de [`src/dashboard.py`](../../src/dashboard.py) y [`docker-compose.yml`](../../docker-compose.yml).

---

## Requisitos

### 1. PostgreSQL corriendo en Docker

El dashboard consulta directamente la base de datos PostgreSQL cargada en Fase 3. El contenedor debe estar activo:

```bash
docker compose up -d
```

Verificar:

```bash
docker ps --filter name=olist_postgres
```

### 2. Datos cargados

Si la base de datos esta vacia, ejecutar el pipeline de carga:

```bash
python src/load_to_db.py
```

### 3. Dependencias de Python

```bash
pip install streamlit plotly sqlalchemy psycopg2-binary pandas
```

---

## Ejecucion

```bash
streamlit run src/dashboard.py
```

El dashboard se abre automaticamente en el navegador en `http://localhost:8501`.

---

## Conexion a Base de Datos

La conexion esta definida en `src/dashboard.py`:

```
postgresql://olist:olist123@localhost:5433/olist
```

Si PostgreSQL esta corriendo en un puerto diferente, modificar la variable `DB_URL` en la linea 13 del archivo.

---

## Cache

El dashboard usa dos niveles de cache de Streamlit:

| Decorator | Aplicado a | TTL |
|-----------|------------|-----|
| `@st.cache_resource` | `get_engine()` | Indefinido (conexion reutilizada) |
| `@st.cache_data` | `run_query()` | 600 segundos (10 minutos) |

Esto significa que las queries SQL se ejecutan una vez y se reutilizan durante 10 minutos. Para forzar una recarga, usar el boton "Rerun" de Streamlit o limpiar cache desde el menu.
