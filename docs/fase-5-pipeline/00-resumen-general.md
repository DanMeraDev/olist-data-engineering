# Fase 5 — Pipeline End-to-End

**Dataset:** Olist Brazilian E-Commerce (Kaggle)
**Objetivo:** Automatizar el flujo completo de datos con un solo comando: desde la limpieza de CSVs hasta el envio del reporte a Telegram y el lanzamiento del dashboard.

> Todos los datos presentados fueron extraidos de [`src/run_pipeline.py`](../../src/run_pipeline.py), [`docker-compose.yml`](../../docker-compose.yml) y [`n8n/olist_workflow.json`](../../n8n/olist_workflow.json).

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| Orquestador | Python (`subprocess`) |
| Limpieza | Pandas |
| Base de datos | PostgreSQL 16 en Docker (puerto 5433) |
| Automatizacion | n8n en Docker (puerto 5678) |
| Notificaciones | Telegram Bot API |
| Dashboard | Streamlit + Plotly |
| Infraestructura | Docker Compose |

---

## Arquitectura del Pipeline

El pipeline ejecuta 4 pasos en secuencia:

```
python src/run_pipeline.py
        |
        v
  Paso 1: Limpieza (run_cleaning.py)
        |
        v
  Paso 2: Carga a PostgreSQL (load_to_db.py)
        |
        v
  Paso 3: Reporte a Telegram (n8n webhook)
        |
        v
  Paso 4: Dashboard Streamlit (localhost:8501)
```

Si algun paso falla, el pipeline se detiene inmediatamente e informa el error. No se ejecutan los pasos siguientes.

---

## Que Automatiza el Pipeline

### Sin pipeline (manual)

1. Ejecutar `python src/run_cleaning.py` y esperar a que termine
2. Ejecutar `python src/load_to_db.py` y esperar a que termine
3. Abrir n8n en el navegador (`localhost:5678`)
4. Disparar el workflow manualmente desde la interfaz
5. Esperar a que el reporte llegue a Telegram
6. Abrir otra terminal
7. Ejecutar `streamlit run src/dashboard.py`
8. Si algo falla en el camino, investigar en cual paso ocurrio el error

### Con pipeline (automatizado)

```bash
python src/run_pipeline.py
```

Un solo comando que:
- Ejecuta los 4 pasos en secuencia automaticamente
- Valida que cada paso termine correctamente antes de continuar
- Si alguno falla, detiene la ejecucion e informa exactamente donde ocurrio el error
- El dashboard queda corriendo hasta que el usuario presione `Ctrl+C`

---

## Como Ejecutar

### Prerequisitos

1. Docker corriendo con los contenedores levantados:

```bash
docker compose up -d
```

2. Dependencias de Python instaladas:

```bash
pip install pandas sqlalchemy "psycopg[binary]" requests streamlit plotly
```

3. n8n configurado con credenciales de PostgreSQL y Telegram (ver [02-configuracion-n8n.md](./02-configuracion-n8n.md))

### Ejecutar el pipeline

```bash
python src/run_pipeline.py
```

El webhook de n8n es configurable via variable de entorno:

```bash
N8N_WEBHOOK_URL=http://localhost:5678/webhook/olist-pipeline
```

---

## Archivos Clave

| Archivo | Funcion |
|---------|---------|
| `src/run_pipeline.py` | Script maestro que orquesta los 4 pasos |
| `src/run_cleaning.py` | Paso 1: limpieza de 9 CSVs |
| `src/load_to_db.py` | Paso 2: carga a PostgreSQL |
| `n8n/olist_workflow.json` | Paso 3: workflow de n8n (queries + Telegram) |
| `src/dashboard.py` | Paso 4: dashboard Streamlit |
| `docker-compose.yml` | Infraestructura Docker (PostgreSQL + n8n) |
