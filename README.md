# Olist E-Commerce — Data Engineering

**Prueba Tecnica — Data Engineer Intern**
Posicion: Data Engineer Intern | Area: Ingenieria de Datos · Invers AI
Realizado por: **Daniel Mera**

Proyecto de data engineering end-to-end sobre el dataset [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) de Kaggle (**Dataset A**) — ~100k ordenes reales anonimizadas distribuidas en 9 CSVs relacionados: clientes, pedidos, pagos, vendedores, productos, resenas y geolocalizacion.

El pipeline completo cubre desde la exploracion y limpieza de datos crudos hasta la carga en PostgreSQL, generacion de reportes automaticos a Telegram via n8n, y visualizacion en un dashboard interactivo con Streamlit.

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| Lenguaje | Python 3 |
| Analisis de datos | Pandas, NumPy |
| Visualizacion (notebooks) | Matplotlib, Seaborn |
| Base de datos | PostgreSQL 16 (Docker) |
| ORM / Conexion DB | SQLAlchemy + psycopg |
| Automatizacion | n8n (Docker) |
| Notificaciones | Telegram Bot API |
| Dashboard | Streamlit + Plotly |
| Infraestructura | Docker Compose |
| Entorno | Windows 11 + Git Bash |

---

## Estructura del Proyecto

```
olist-data-engineering/
├── data/
│   ├── raw/                  # 9 CSVs originales de Kaggle (incluidos en el repo)
│   └── clean/                # 9 CSVs limpios (no incluidos, se generan al ejecutar el pipeline)
├── docs/
│   ├── fase-1-exploracion/   # Exploracion de cada dataset
│   ├── fase-2-limpieza/      # Decisiones y transformaciones de limpieza
│   ├── fase-3-modelado/      # Esquema relacional e infraestructura
│   ├── fase-4-dashboard/     # Preguntas de negocio y visualizaciones
│   └── fase-5-pipeline/      # Pipeline end-to-end y configuracion n8n
├── notebooks/
│   ├── 01_exploracion_diagnostico.ipynb
│   └── 02-limpieza_y_transformacion.ipynb
├── n8n/
│   └── olist_workflow.json   # Workflow de n8n (queries + Telegram)
├── sql/
│   ├── schema.sql            # DDL: tablas, PKs, FKs, indices
│   └── init-n8n-db.sh        # Script para crear la DB de n8n
├── src/
│   ├── cleaning/             # Modulos de limpieza por dataset
│   ├── run_cleaning.py       # Ejecuta toda la limpieza (Fase 2)
│   ├── load_to_db.py         # Carga datos a PostgreSQL (Fase 3)
│   ├── dashboard.py          # Dashboard Streamlit (Fase 4)
│   └── run_pipeline.py       # Pipeline completo end-to-end (Fase 5)
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Documentacion por Fase

Toda la documentacion detallada se encuentra en la carpeta `docs/`. Cada carpeta contiene un `00-resumen-general.md` como punto de entrada.

| Fase | Carpeta | Descripcion |
|------|---------|-------------|
| **Fase 1** | [`docs/fase-1-exploracion/`](docs/fase-1-exploracion/) | Exploracion de los 9 datasets: estructura, tipos de datos, nulos, duplicados, distribuciones y hallazgos por cada CSV |
| **Fase 2** | [`docs/fase-2-limpieza/`](docs/fase-2-limpieza/) | Decisiones de limpieza, transformaciones aplicadas (normalizacion de ciudades, correccion de typos, conversion de fechas, eliminacion de duplicados) y verificacion post-limpieza |
| **Fase 3** | [`docs/fase-3-modelado/`](docs/fase-3-modelado/) | Diseno del esquema relacional en PostgreSQL (de 9 CSVs a 8 tablas), decisiones de modelado, infraestructura Docker e instrucciones de carga |
| **Fase 4** | [`docs/fase-4-dashboard/`](docs/fase-4-dashboard/) | 5 preguntas de negocio respondidas con visualizaciones interactivas en Streamlit + Plotly, conectadas directamente a PostgreSQL |
| **Fase 5** | [`docs/fase-5-pipeline/`](docs/fase-5-pipeline/) | Pipeline end-to-end con un solo comando, configuracion de n8n y Telegram, detalle del reporte automatico |

---

## Guia de Instalacion y Ejecucion

### Prerequisitos

- **Python 3.10+**
- **Docker Desktop** instalado y corriendo
- **Git Bash** (en Windows) u otra terminal con soporte para comandos Unix

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd olist-data-engineering
```

Los 9 CSVs originales de Kaggle ya estan incluidos en `data/raw/`, no es necesario descargarlos aparte.

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/Scripts/activate    # En Git Bash (Windows)
pip install -r requirements.txt
```

### 3. Levantar la infraestructura Docker

```bash
docker compose up -d
```

Esto levanta dos contenedores:
- **PostgreSQL 16** en puerto `5433` (base de datos `olist`)
- **n8n** en puerto `5678` (interfaz web de automatizacion)

Verificar que estan corriendo:

```bash
docker ps --filter name=olist
```

> Detalle completo de la infraestructura Docker en [`docs/fase-3-modelado/03-infraestructura.md`](docs/fase-3-modelado/03-infraestructura.md).

### 4. Configurar n8n y Telegram

Para que el reporte automatico a Telegram funcione, n8n debe estar configurado **antes** de ejecutar el pipeline:

1. Abrir `http://localhost:5678` y crear una cuenta local
2. Importar el workflow desde `n8n/olist_workflow.json`
3. Configurar credenciales de PostgreSQL en n8n (host: `postgres`, puerto: `5432`)
4. Crear bot de Telegram con `@BotFather`, obtener token y chat_id
5. Configurar credenciales de Telegram en n8n
6. Activar el workflow (toggle en la esquina superior derecha)

> Guia paso a paso completa con capturas y detalles en [`docs/fase-5-pipeline/02-configuracion-n8n.md`](docs/fase-5-pipeline/02-configuracion-n8n.md).

> Si se prefiere omitir este paso, el pipeline igual funciona — ejecuta limpieza, carga y dashboard, y solo muestra una advertencia al intentar enviar el reporte a Telegram.

### 5. Ejecutar el pipeline completo

```bash
python src/run_pipeline.py
```

Este comando ejecuta los 4 pasos en secuencia:

1. **Limpieza** — Lee 9 CSVs de `data/raw/`, aplica transformaciones y genera 9 CSVs limpios en `data/clean/`
2. **Carga a PostgreSQL** — Crea el esquema y carga 8 tablas en la base de datos
3. **Reporte a Telegram** — Dispara el workflow de n8n que envia KPIs a Telegram
4. **Dashboard** — Lanza Streamlit en `http://localhost:8501`

Si alguno falla, el pipeline se detiene e informa el error. Presionar `Ctrl+C` para detener el dashboard.

> Arquitectura del pipeline, queries ejecutados y manejo de errores en [`docs/fase-5-pipeline/01-arquitectura-pipeline.md`](docs/fase-5-pipeline/01-arquitectura-pipeline.md).
> Detalle del reporte de Telegram (KPIs, categorias, logistica, incidencias) en [`docs/fase-5-pipeline/03-reporte-telegram.md`](docs/fase-5-pipeline/03-reporte-telegram.md).

### Ejecucion paso a paso (opcional)

Si se prefiere ejecutar cada fase por separado en lugar del pipeline completo:

```bash
# Fase 2: Solo limpieza
python src/run_cleaning.py
```
> Transformaciones aplicadas en [`docs/fase-2-limpieza/02-limpieza-por-dataset.md`](docs/fase-2-limpieza/02-limpieza-por-dataset.md).

```bash
# Fase 3: Solo carga a PostgreSQL
python src/load_to_db.py
```
> Esquema de tablas y decisiones de modelado en [`docs/fase-3-modelado/02-esquema-tablas.md`](docs/fase-3-modelado/02-esquema-tablas.md).

```bash
# Fase 4: Solo dashboard
streamlit run src/dashboard.py
```
> Preguntas de negocio y hallazgos en [`docs/fase-4-dashboard/01-preguntas-y-hallazgos.md`](docs/fase-4-dashboard/01-preguntas-y-hallazgos.md).

---

## Conexion a PostgreSQL

Desde cualquier cliente SQL:

```
Host:     localhost
Puerto:   5433
Database: olist
Usuario:  olist
Password: olist123
```

Connection string:

```
postgresql://olist:olist123@localhost:5433/olist
```

> Instrucciones para conectarse, reiniciar desde cero y mas en [`docs/fase-3-modelado/03-infraestructura.md`](docs/fase-3-modelado/03-infraestructura.md).
